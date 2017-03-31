import types
from opcode import opname
from queue import LifoQueue
import time
from dis import HAVE_ARGUMENT

from zope.interface import Interface
from zope.interface.interface import Method
from zope.interface.verify import verifyObject, verifyClass

from TimeClock import Utils
from TimeClock.Report.Access.AFunction import AFunction
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible
from TimeClock.Util import BoundFunction, OverloadedMethod, AnnotatedMethod
from .Function import Function


class LifoQueue(LifoQueue):
    def __init__(self):
        super().__init__()

    def __getitem__(self, item):
        return self.queue[item]

    def __setitem__(self, item, val):
        self.queue[item] = val

    def get(self):
        return super().get(False)


class Sandbox(object):
    SUSPEND_TIME = object()
    SUSPEND_INST = object()
    PRIMITIVE = object()
    FUNCTION = object()
    startTime = None
    counter = None
    iterlimit = None
    timelimit = None
    sub = None

    def __init__(self, parent, function, arguments, *, globals_=None, interfaces=()):
        self.parent = parent
        if globals_ is None:
            globals_ = {}
        if parent:
            self.stack = parent.stack
            self.blocks = parent.blocks
            self.frames = parent.frames
            self.globals = parent.globals
            self.interfaces = parent.interfaces
        else:
            self.stack = LifoQueue()
            self.blocks = LifoQueue()
            self.frames = LifoQueue()
            self.globals = globals_
            self.interfaces = interfaces
        self.local_variables = {}
        self.function = function
        self.arguments = arguments
        self.index = 0

    def loadName(self, name):
        if name in self.local_variables:
            return self.local_variables[name]
        closure = self.function.closure
        while closure:
            if name in closure.local_variables:
                return closure.local_variables[name]
            closure = closure.function.closure
        if name in self.globals:
            return self.globals[name]
        raise NameError("%s is not defined" % name)

    def getAttr(self, obj, attr):
        try:
            verifyObject(IAbstractAccessible, obj)
        except:
            print(79, obj, type(obj), attr)
            raise
        for iface in obj.__implemented__.interfaces():
            if issubclass(iface, IAbstractAccessible) and attr in iface:
                if isinstance(iface[attr], (Method,)):
                    return AFunction(getattr(obj, attr))
                return getattr(obj, attr)
        print(82, obj, attr)
        raise AttributeError("%r attribute access denied" % type(obj))

    def storeName(self, name, value):
        self.local_variables[name] = value

    def callFunction(self, function, arguments, keywords=None):
        if keywords is None:
            keywords = {}
        if isinstance(function, AFunction):
            return [function.TYPE, function.function, arguments] + ([keywords] if keywords is not None else [])
        if isinstance(function, Function):
            return [self.FUNCTION, function, arguments]
        if Utils.issubclass(function, IAbstractAccessible):
            return [self.PRIMITIVE, function, arguments, keywords]
        raise TypeError("Function %r not allowed" % function)

    def execute(self, iterlimit, timelimit):
        self.startTime = time.time()
        self.counter = 0
        self.iterlimit = iterlimit
        self.timelimit = timelimit
        if hasattr(self.function, 'arguments') and len(self.arguments) != len(self.function.arguments):
            raise TypeError("%r expects %i arguments, got %i" % (
                self.function,
                len(self.function.arguments),
                len(self.arguments)))
        for idx, i in enumerate(self.function.arguments):
            v = self.arguments[idx]
            if isinstance(i, tuple):
                t = i[1]
                i = i[0]
                i = i.title().replace(' ', '')
                i = i[0].lower() + i[1:]
                if v == 'None':
                    self.local_variables[i] = None
                    continue
                t = self.loadName(t)
                v = self.callFunction(t, [v])
                v = v[1](*v[2], **v[3])

            self.local_variables[i] = v
        while True:
            self.counter += 1
            now = time.time()
            if now - self.startTime > self.timelimit:
                self.timelimit += yield self.SUSPEND_TIME
            if self.counter > self.iterlimit:
                self.iterlimit += yield self.SUSPEND_INST
            opcode = self.function[self.index]
            if opcode >= HAVE_ARGUMENT:
                args = self.function[self.index + 1:self.index + 3]
                self.index += 3
            else:
                args = []
                self.index += 1
            operation = opname[opcode]
            function = OpMap.getOp(operation)
            ret = function(self, args)
            if ret == OpMap.CALLFUNCTION:
                func = self.stack.get()
                typ = func[0]
                if typ is self.PRIMITIVE:
                    func, args, kw = func[1:]
                    self.stack.put(func(*args, **kw))
                elif typ is self.FUNCTION:
                    func, args, *_ = func[1:]
                    self.sub = sb = Sandbox(self, func, args)
                    gen = sb.execute(self.iterlimit - self.counter, self.timelimit + self.startTime - time.time())
                    n = next(gen)
                    while n is self.SUSPEND_INST or n is self.SUSPEND_TIME:
                        r = yield n
                        n = gen.send(r)
                    self.sub = None
                    self.stack.put(n)

            elif ret != OpMap.NORETURN:
                yield ret


from .OpMap import OpMap
