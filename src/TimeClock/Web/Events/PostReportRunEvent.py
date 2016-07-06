from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportEvent import IReportEvent
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IReportEvent)
class PostReportRunEvent(WebEvent):
    @coerce
    def __init__(self, sa: IReport, format_: IFormat, args, result, caller: IEmployee):
        self.report = sa
        self.format = format_
        self.args = args
        self.result = result
        self.caller = caller
    def getType(self):
        return IReportEvent
