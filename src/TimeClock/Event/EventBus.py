from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import coerce
from axiom.attributes import text
from zope.interface import implementer, Interface

from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from axiom.item import Item


@implementer(IEventBus)
class EventBus(Item):
    name = text()
    def postEvent(self, event: IEvent) -> bool:
        handlers = self.getEventHandlers(event)
        for handler in handlers:
            handler.handleEvent(event)
            if event.cancellable and event.cancelled:
                return False
            if event.getFinished():
                return True
        return True

    @coerce
    def getEventHandlers(self, event: IEvent) -> [IEventHandler]:
        iet = event.getType()
        bases = [iet]
        toProcess = [iet]
        while toProcess:
            iet = toProcess.pop()
            for i in iet.getBases():
                if i is Interface:
                    continue
                if i not in bases:
                    bases.append(i)
                    toProcess.append(i)
        for b in bases:
            yield from self.powerupsFor(b)






    @coerce
    def register(self, handler: IEventHandler, eventType: Subclass[IEvent]) -> bool:
        if handler in list(self.powerupsFor(eventType)):
            return False
        if isinstance(handler, Item):
            self.powerUp(handler, eventType)
            self.powerUp(handler, IEventHandler)
        else:
            self.inMemoryPowerUp(handler, eventType)
            self.inMemoryPowerUp(handler, IEventHandler)
        return True

    def unregister(self, handler: IEventHandler, eventType: Subclass[IEvent]=None) -> bool:
        if isinstance(handler, Item):
            if eventType is None:
                for eventType in self.interfacesFor(handler):
                    self.powerDown(handler, eventType)
                return True
            self.powerDown(handler, eventType)
            if len(self.interfacesFor(handler)) == 1:
                self.powerDown(handler, IEventHandler)
        else:
            if eventType is None:
                for iface, pups in self._inMemoryPowerups.items():
                    if handler in pups:
                        pups.remove(handler)
                return True
            if handler in self.powerupsFor(eventType):
                self._inMemoryPowerups[eventType].remove(handler)
            for iface, pups in self._inMemoryPowerups.items():
                if handler in pups and iface is not IEventHandler:
                    break
            else:
                self._inMemoryPowerups[IEventHandler].remove(handler)
        return True


def findEventBus(name: str) -> IEventBus:
    return Store.Store.findOrCreate(EventBus, name=name)

registerAdapter(findEventBus, str, IEventBus)
