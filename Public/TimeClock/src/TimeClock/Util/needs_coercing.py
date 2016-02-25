from zope.interface import Interface

from TimeClock.Util.subclass import subclass


def needs_coercing(Variable, Type):
    if isinstance(Type, subclass):
        if issubclass(Variable, Type.cls):
            return False
        return True
    if isinstance(Variable, Type):
        return False
    if issubclass(Type, Interface) and Type.providedBy(Variable):
        return False
    return True
