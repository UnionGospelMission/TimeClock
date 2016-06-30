from zope.interface import implementer

from TimeClock.Event.AbstractEvent import AbstractEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


@implementer(IWebEvent)
class WebEvent(AbstractEvent):
    def getType(self) -> IWebEvent:
        return IWebEvent


