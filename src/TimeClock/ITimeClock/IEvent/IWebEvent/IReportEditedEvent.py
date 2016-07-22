from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class IReportEditedEvent(IWebEvent):
    report = Attribute("report")
    new_code = Attribute("new_code")
