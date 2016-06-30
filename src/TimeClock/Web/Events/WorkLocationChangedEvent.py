from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IWebEvent.IWorkLocationChangedEvent import IWorkLocationChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IWorkLocationChangedEvent)
class WorkLocationChangedEvent(WebEvent):
    @coerce
    def __init__(self, sa: IWorkLocation, previous_values):
        self.workLocation = sa
        self.previous_values = previous_values
    def getType(self):
        return IWorkLocationChangedEvent
