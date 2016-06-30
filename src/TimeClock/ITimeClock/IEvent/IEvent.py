from zope.interface import Interface, Attribute

from TimeClock.Util import fromFunction
from TimeClock.Util.subclass import Subclass


class IEvent(Interface):
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


def getType() -> Subclass[IEvent]:
    pass

IEvent.getType = fromFunction(getType)
