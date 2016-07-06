import time
from zope.interface import implementer

from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IEvent.IWebEvent.ITimeEntryChangedEvent import ITimeEntryChangedEvent
from TimeClock.Utils import overload
from TimeClock.Web.Events.TimeEntryChangedEvent import TimeEntryChangedEvent


web = IEventBus("Web")


@implementer(IEventHandler)
class TimeEntryValidator(object):
    def __init__(self):
        web.register(self, ITimeEntryChangedEvent)
    def powerUp(self, object, iface):
        pass
    @overload
    def handleEvent(self, event: TimeEntryChangedEvent):
        timeEntry = event.timeEntry
        if timeEntry.startTime() > timeEntry.endTime():
            event.cancel()
            event.setReturn("Start time set to after end time for shift beginning at %s" % str(event.previous_values.get('startTime', timeEntry.startTime())))
            return
        if timeEntry.endTime() > IDateTime(time.time()):
            event.cancel()
            event.setReturn("End time is in the future")
            return

    @overload
    def handleEvent(self, event: IEvent):
        pass

tev = TimeEntryValidator()
