from zope.interface import Interface

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IEvent.IEvent import IEvent


class IEventHandler(IItem):
    def handleEvent(event: IEvent):
        pass
