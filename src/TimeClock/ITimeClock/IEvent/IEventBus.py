from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.Util.subclass import Subclass


class IEventBus(IItem):
    def getEventHandlers(event: IEvent) -> [IEventHandler]:
        pass

    def postEvent(event: IEvent) -> object:
        pass

    def register(handler: IEventHandler, eventType: Subclass[IEvent]) -> bool:
        pass

    def unregister(handler: IEventHandler, eventType: Subclass[IEvent]=None):
        pass

    name = Attribute("name")
