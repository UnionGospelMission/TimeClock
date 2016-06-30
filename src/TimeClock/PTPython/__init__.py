import sys

from ptpython.repl import PythonRepl

import TimeClock
from axiom import store
from twisted.internet import reactor
import atexit



try:
    from .TwistedEventLoop import TwistedEventLoop
    from .TwistedPythonCommandLineInterface import TwistedPythonCommandLineInterface
except ImportError:
    TwistedEventLoop = None
    TwistedPythonCommandLineInterface = None

embedded = False
reembed = False
stopper = None
loop = None


def iterate(cli, inp):
    global embedded, reembed
    try:
        z = inp.send(True)
        if isinstance(z, TwistedEventLoop.NOTDONE):
            reactor.callLater(z.delay, iterate, cli, inp)
            return True
    except StopIteration:
        embedded = False
        reembed = True
        try:
            next(cli)
        except StopIteration:
            pass
        embed()
    except SystemExit:
        reactor.stop()
    except Exception as e:
        print(37, e)
        reactor.stop()


def cleanup(cli):
    try:
        next(cli)
    finally:
        cli.rm.__exit__()
        cli._redraw()


def getloop():
    return loop


def fixOffsets(ops, incr):
    from dis import HAVE_ARGUMENT, opname, hasjabs
    itr = enumerate(iter(ops))
    for idx, i in itr:
        if i < HAVE_ARGUMENT:
            continue
        name = opname[i]
        arg = next(itr)[1] + next(itr)[1] * 256
        if i in hasjabs:
            print('fixing opcode', name, arg, arg + incr)
            arg += incr
            ops[idx + 1] = arg % 256
            ops[idx + 2] = arg // 256





def patchStop(func):
    from dis import opmap
    code = func.__code__.__class__
    c = func.__code__
    oldops = bytearray(c.co_code)
    consts = c.co_consts + (getloop, False)
    names = c.co_names + ('_running',)
    loopidx = len(consts) - 2
    constidx = len(names) - 1
    constval = len(consts) - 1

    newops = bytearray([
        opmap['LOAD_CONST'], constval % 256, constval // 256,
        opmap['LOAD_CONST'], loopidx % 256, loopidx // 256,
        opmap['CALL_FUNCTION'], 0, 0,
        opmap['STORE_ATTR'], constidx % 256, constidx // 256,

    ])
    lnotab = bytearray(c.co_lnotab)
    lnotab.insert(0, 0)
    lnotab.insert(0, len(newops))
    fixOffsets(oldops, len(newops))
    newcode = code(c.co_argcount, c.co_kwonlyargcount, c.co_nlocals, c.co_stacksize, c.co_flags, bytes(newops+oldops), consts,
                   names, c.co_varnames, c.co_filename, c.co_name, c.co_firstlineno, bytes(lnotab), c.co_freevars,
                   c.co_cellvars)
    func.__code__ = newcode


def embed():
    global embedded, stopper, loop
    if (not embedded or reembed) and TwistedPythonCommandLineInterface and sys.stdin.isatty():
        embedded = True
        locs = {
            'db': TimeClock.Axiom.Store.Store,
            'store': store,
            'TimeClock': TimeClock
        }
        repl = PythonRepl(lambda: locs, lambda: locs, vi_mode=False, history_filename='console.history')
        loop = TwistedEventLoop()
        cli = TwistedPythonCommandLineInterface(python_input=repl, eventloop=loop).run()
        inp = next(cli)
        atexit.register(cleanup, cli)
        next(inp)

        reactor.callLater(0.1, iterate, cli, inp)
        if not reembed:
            patchStop(reactor.stop.__func__)
        sys.stdout = open(1, 'w')
    else:
        print("Not embedding console", embedded, TwistedPythonCommandLineInterface, sys.stdin.isatty())

