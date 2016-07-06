from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class IReportChangedEvent(IWebEvent):
    report = Attribute("report")
    previous_values = Attribute("previous_values")
