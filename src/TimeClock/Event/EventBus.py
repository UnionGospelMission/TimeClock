from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.IEvent.IAbstractEvent import IAbstractEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from axiom.item import Item


@implementer(IEventBus)
class EventBus(Item):
    name = text()
    def postEvent(self, event: IAbstractEvent) -> bool:
        handlers = self.getEventHandlers(event)
        for handler in handlers:
            handler.handleEvent(event)
            if event.cancellable and event.cancelled:
                return False
            if event.getFinished():
                return True
        return True

    def getEventHandlers(self, event: IAbstractEvent) -> [IEventHandler]:
        iet = event.getType()
        return self.powerupsFor(iet)


def findEventBus(name: str) -> IEventBus:
    return Store.Store.findOrCreate(EventBus, name=name)

registerAdapter(findEventBus, str, IEventBus)
