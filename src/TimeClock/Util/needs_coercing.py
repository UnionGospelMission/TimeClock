from zope.interface import Interface

from TimeClock.Util.subclass import subclass


def needs_coercing(Variable, Type):
    if Variable is None:
        return False
    if isinstance(Type, list):
        if not isinstance(Variable, list):
            return True
        for v in Variable:
            if needs_coercing(v, Type[0]):
                return True
        return False
    if isinstance(Type, subclass):
        if issubclass(Variable, Type.cls):
            return False
        return True
    try:
        if isinstance(Variable, Type):
            return False
    except:
        print(17, Variable, Type)
        raise
    if issubclass(Type, Interface) and Type.providedBy(Variable):
        return False
    return True
