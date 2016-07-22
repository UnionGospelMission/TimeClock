from zope.interface import implementer

from TimeClock.ITimeClock.IEvent.IWebEvent.IReportEditedEvent import IReportEditedEvent
from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IReportEditedEvent)
class ReportEditedEvent(WebEvent):
    @coerce
    def __init__(self, sa: IReport, new_code):
        self.report = sa
        self.new_code = new_code
    def getType(self):
        return IReportEditedEvent
