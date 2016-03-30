from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IEvent.IAbstractEvent import IAbstractEvent
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler


class IEventBus(IItem):
    def getEventHandlers(event: IAbstractEvent) -> [IEventHandler]:
        pass

    def postEvent(event: IAbstractEvent) -> object:
        pass

    name = Attribute("name")
