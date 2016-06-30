from ptpython.python_input import PythonCommandLineInterface


class TwistedPythonCommandLineInterface(PythonCommandLineInterface):
    NOTDONE = object()
    _exit_flag = False
    def run(self, reset_current_buffer=False, pre_run=None):
        """
        Read input from the command line.
        This runs the eventloop until a return value has been set.

        :param reset_current_buffer: Reset content of current buffer.
        :param pre_run: Callable that is called right after the reset has taken
            place. This allows custom initialisation.
        """
        assert pre_run is None or callable(pre_run)

        try:
            self._is_running = True

            self.on_start.fire()
            self.reset(reset_current_buffer=reset_current_buffer)

            # Call pre_run.
            if pre_run:
                pre_run()

            # Run eventloop in raw mode.
            with self.input.raw_mode() as rm:
                self.rm = rm
                self.renderer.request_absolute_cursor_position()
                self._redraw()

                yield self.eventloop.run(self.input, self.create_eventloop_callbacks())
        finally:
            # Clean up renderer. (This will leave the alternate screen, if we use
            # that.)

            # If exit/abort haven't been called set, but another exception was
            # thrown instead for some reason, make sure that we redraw in exit
            # mode.
            if not self.is_done:
                self._exit_flag = True
                self._redraw()

            self.renderer.reset()
            self.on_stop.fire()
            self._is_running = False

        # Return result.
        yield self.return_value()

