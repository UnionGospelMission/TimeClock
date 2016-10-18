import types

from TimeClock.Util import BoundFunction
from TimeClock.Utils import coerce


class AFunction(object):
    __slots__ = ['_parent', 'function', 'TYPE']

    @coerce
    def __init__(self, function):
        from TimeClock.Sandbox.Sandbox import Sandbox

        self.function = function
        if isinstance(function, types.BuiltinFunctionType):
            self.TYPE = Sandbox.PRIMITIVE
        elif isinstance(function, (types.MethodType, BoundFunction)):
            self.TYPE = Sandbox.PRIMITIVE
        else:
            self.TYPE = Sandbox.FUNCTION
