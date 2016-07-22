import types
from opcode import opname
from queue import LifoQueue
import time
from dis import HAVE_ARGUMENT

from zope.interface import Interface
from zope.interface.verify import verifyObject, verifyClass

from TimeClock import Utils
from TimeClock.Util import BoundFunction
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

    def __init__(self, parent, function, arguments, *, globals_=None, functions=(), attributes_accessible = ()):
        self.parent = parent
        if globals_ is None:
            globals_ = {}
        if parent:
            self.stack = parent.stack
            self.blocks = parent.blocks
            self.frames = parent.frames
            self.globals = parent.globals
            self.functions = parent.functions
            self.attributes_accessible = parent.attributes_accessible
        else:
            self.stack = LifoQueue()
            self.blocks = LifoQueue()
            self.frames = LifoQueue()
            self.globals = globals_
            self.functions = functions
            self.attributes_accessible = attributes_accessible
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
        if obj in self.attributes_accessible:
            return getattr(obj, attr)
        if type(obj) in self.attributes_accessible:
            return getattr(obj, attr)
        for i in self.attributes_accessible:
            if isinstance(i, Interface) or Utils.issubclass(i, Interface):
                try:
                    verifyObject(i, obj)
                except:
                    try:
                        verifyClass(i, obj)
                    except:
                        continue
                if attr in i:
                    return getattr(obj, attr)
                else:
                    AttributeError("%r interface attribute access denied for %s" % type(obj, attr))
        raise AttributeError("%r attribute access denied" % type(obj))

    def storeName(self, name, value):
        self.local_variables[name] = value

    def callFunction(self, function, arguments, keywords=None):
        if keywords is None:
            keywords = {}
        if function in self.functions:
            return [self.PRIMITIVE, function, arguments, keywords]
        if isinstance(function, types.BuiltinFunctionType) and function.__self__ is not None:
            for i in self.functions:
                if hasattr(i, '__get__') and i.__get__(function.__self__) == function:
                    return [self.PRIMITIVE, function, arguments, keywords]
        if isinstance(function, (types.MethodType, BoundFunction)):
            for i in self.functions:
                if not isinstance(i, BoundFunction):
                    continue
                if i.__func__ is function.__func__ and i.oself is None:
                    return [self.PRIMITIVE, function, arguments, keywords]
            if function.__func__ in self.functions:
                return [self.PRIMITIVE, function, arguments, keywords]
        if keywords:
            raise TypeError("keyword arguments unsupported")
        if type(function) == Function:
            return [self.FUNCTION, function, arguments]
        raise TypeError("Function %r not allowed" %function)

    def execute(self, iterlimit, timelimit):
        self.startTime = time.time()
        self.counter = 0
        self.iterlimit = iterlimit
        self.timelimit = timelimit
        if len(self.arguments) != len(self.function.arguments):
            raise TypeError("%r expects %i arguments, got %i" % (
                self.function,
                len(self.function.arguments),
                len(self.arguments)))
        for idx, i in enumerate(self.function.arguments):
            v = self.arguments[idx]
            if isinstance(i, tuple):
                i, t = i
                i = i.title().replace(' ', '')
                i = i[0].lower() + i[1:]
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
                    func, args = func[1:]
                    sb = Sandbox(self, func, args)
                    gen = sb.execute(self.iterlimit - self.counter, self.timelimit + self.startTime - time.time())
                    n = next(gen)
                    while n is self.SUSPEND_INST or n is self.SUSPEND_TIME:
                        r = yield n
                        n = gen.send(r)
                    print(166, n)
                    self.stack.put(n)

            elif ret != OpMap.NORETURN:
                yield ret


from .OpMap import OpMap
