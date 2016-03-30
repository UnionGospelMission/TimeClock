from zope.interface import Interface, Attribute

from TimeClock.Util.subclass import Subclass


class IAbstractEvent(Interface):
    cancellable = Attribute("cancellable")
    cancelled = Attribute("cancelled")

    def cancel() -> bool:
        pass

    def setReturn(retval: object) -> bool:
        pass

    def setFinished(finished: bool) -> bool:
        pass

    def getFinished() -> bool:
        pass


def getType() -> Subclass[IAbstractEvent]:
    pass

IAbstractEvent.getType = getType
