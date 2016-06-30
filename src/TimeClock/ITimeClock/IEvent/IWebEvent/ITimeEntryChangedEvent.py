from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class ITimeEntryChangedEvent(IWebEvent):
    timeEntry = Attribute("timeEntry")
    previous_values = Attribute("previous_values")
