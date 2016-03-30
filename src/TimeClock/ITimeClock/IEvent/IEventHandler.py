from zope.interface import Interface

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IEvent.IAbstractEvent import IAbstractEvent


class IEventHandler(IItem):
    def handleEvent(event: IAbstractEvent):
        pass
