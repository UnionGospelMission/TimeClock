from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.IWorkLocationChangedEvent import IWorkLocationChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(ITimeEntryChangedEvent)
class TimeEntryChangedEvent(WebEvent):
    @coerce
    def __init__(self, sa: ITimeEntry, previous_values):
        self.timeEntry = sa
        self.previous_values = previous_values
    def getType(self):
        return ITimeEntryChangedEvent
