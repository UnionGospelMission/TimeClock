import os
import random
import select

import errno

import datetime
from prompt_toolkit.eventloop.callbacks import EventLoopCallbacks
from prompt_toolkit.eventloop.posix import PosixEventLoop, call_on_sigwinch
from prompt_toolkit.eventloop.posix_utils import PosixStdinReader
from prompt_toolkit.eventloop.utils import TimeIt
from prompt_toolkit.input import Input
from prompt_toolkit.terminal.vt100_input import InputStream
from prompt_toolkit.utils import in_main_thread, DummyContext


_now = datetime.datetime.now


def _select(*args, **kwargs):
    """
    Wrapper around select.select.

    When the SIGWINCH signal is handled, other system calls, like select
    are aborted in Python. This wrapper will retry the system call.
    """
    while True:
        try:
            return select.select(*args, **kwargs)
        except select.error as e:
            # Retry select call when EINTR
            if e.args and e.args[0] == errno.EINTR:
                continue
            else:
                raise


INPUT_TIMEOUT = 0.1


class TwistedEventLoop(PosixEventLoop):
    def run_as_coroutine(self, stdin, callbacks):
        raise NotImplementedError("This eventloop doesn't implement 'run_as_coroutine()'.")
    class NOTDONE(object):
        def __init__(self, delay):
            self.delay = delay
    def _ready_for_reading(self, timeout=0.1):
        """
        Return the file descriptors that are ready for reading.
        """
        read_fds = list(self._read_fds.keys())
        r, _, _ = _select(read_fds, [], [], timeout)
        return r
    def run(self, stdin, callbacks):
        assert isinstance(stdin, Input)
        assert isinstance(callbacks, EventLoopCallbacks)
        assert not self._running

        if self.closed:
            raise Exception('Event loop already closed.')

        self._running = True
        self._callbacks = callbacks

        inputstream = InputStream(callbacks.feed_key)
        current_timeout = [INPUT_TIMEOUT]  # Nonlocal

        # Create reader class.
        stdin_reader = PosixStdinReader(stdin.fileno())

        # Only attach SIGWINCH signal handler in main thread.
        # (It's not possible to attach signal handlers in other threads. In
        # that case we should rely on a the main thread to call this manually
        # instead.)
        if in_main_thread():
            ctx = call_on_sigwinch(self.received_winch)
        else:
            ctx = DummyContext()

        def read_from_stdin():
            # Feed input text.
            data = stdin_reader.read()
            inputstream.feed(data)

            # Set timeout again.
            current_timeout[0] = INPUT_TIMEOUT

            # Quit when the input stream was closed.
            if stdin_reader.closed:
                self.stop()

        self.add_reader(stdin, read_from_stdin)
        self.add_reader(self._schedule_pipe[0], None)

        with ctx:
            while self._running:
                # Call inputhook.
                with TimeIt() as inputhook_timer:
                    if self._inputhook_context:
                        def ready(wait):
                            return self._ready_for_reading(current_timeout[0] if wait else 0) != []
                        self._inputhook_context.call_inputhook(ready)

                # Calculate remaining timeout. (The inputhook consumed some of the time.)
                if current_timeout[0] is None:
                    remaining_timeout = 0.1
                else:
                    remaining_timeout = max(0, current_timeout[0] - inputhook_timer.duration)

                # Wait until input is ready.
                fds = self._ready_for_reading(remaining_timeout)

                # When any of the FDs are ready. Call the appropriate callback.
                if fds:
                    # Create lists of high/low priority tasks. The main reason
                    # for this is to allow painting the UI to happen as soon as
                    # possible, but when there are many events happening, we
                    # don't want to call the UI renderer 1000x per second. If
                    # the eventloop is completely saturated with many CPU
                    # intensive tasks (like processing input/output), we say
                    # that drawing the UI can be postponed a little, to make
                    # CPU available. This will be a low priority task in that
                    # case.
                    tasks = []
                    low_priority_tasks = []
                    now = _now()

                    for fd in fds:
                        # For the 'call_from_executor' fd, put each pending
                        # item on either the high or low priority queue.
                        if fd == self._schedule_pipe[0]:
                            for c, max_postpone_until in self._calls_from_executor:
                                if max_postpone_until is None or max_postpone_until < now:
                                    tasks.append(c)
                                else:
                                    low_priority_tasks.append((c, max_postpone_until))
                            self._calls_from_executor = []

                            # Flush all the pipe content.
                            os.read(self._schedule_pipe[0], 1024)
                        else:
                            handler = self._read_fds.get(fd)
                            if handler:
                                tasks.append(handler)

                    # Handle everything in random order. (To avoid starvation.)
                    random.shuffle(tasks)
                    random.shuffle(low_priority_tasks)

                    # When there are high priority tasks, run all these.
                    # Schedule low priority tasks for the next iteration.
                    if tasks:
                        for t in tasks:
                            t()

                        # Postpone low priority tasks.
                        for t, max_postpone_until in low_priority_tasks:
                            self.call_from_executor(t, _max_postpone_until=max_postpone_until)
                    else:
                        # Currently there are only low priority tasks -> run them right now.
                        for t, _ in low_priority_tasks:
                            t()

                else:
                    # Flush all pending keys on a timeout. (This is most
                    # important to flush the vt100 'Escape' key early when
                    # nothing else follows.)
                    inputstream.flush()

                    # Fire input timeout event.
                    callbacks.input_timeout()
                    current_timeout[0] = None
                    self._running = yield self.NOTDONE(0.5)

        self.remove_reader(stdin)
        self.remove_reader(self._schedule_pipe[0])

        self._callbacks = None
