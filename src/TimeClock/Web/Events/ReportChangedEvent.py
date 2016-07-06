from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.ITimeClock.IEvent.IWebEvent.IReportChangedEvent import IReportChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IReportChangedEvent)
class ReportChangedEvent(WebEvent):
    @coerce
    def __init__(self, sa: IReport, previous_values):
        self.report = sa
        self.previous_values = previous_values
    def getType(self):
        return IReportChangedEvent
