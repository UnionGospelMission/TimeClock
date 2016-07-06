from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class IReportEvent(IWebEvent):
    report = Attribute("report")
    format = Attribute("format")
    args = Attribute("args")
    result = Attribute("result")
    caller = Attribute("caller")
