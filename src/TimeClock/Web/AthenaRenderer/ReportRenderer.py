from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Report.DynamicReport import DynamicReport
from TimeClock.Report.Format.CSV import CSV
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from nevow.athena import expose
from nevow.loaders import xmlfile
from .Editor import Editor


@implementer(IAthenaRenderable)
class ReportRenderer(AbstractRenderer):
    jsClass = "TimeClock.Reports"
    docFactory = xmlfile(path + '/Pages/ReportRenderer.xml', 'ReportRendererPattern')

    def __init__(self, report: IReport):
        self.report = report
    def render_reportName(self, *a):
        return self.report.name
    def render_reportDescription(self, *a):
        return self.report.description
    @expose
    def viewDetails(self):
        e = Editor(self.report, 'code')
        e.prepare(self)
        e.visible = True
        return e, self.report.name, self.report.description
    @expose
    def save(self, name, description):
        self.report.name = name
        self.report.description = description

    @expose
    def getArgs(self):
        return self.report.getArgs()
    @expose
    def runReport(self, args):
        return self.report.runReport(CSV, args).decode('charmap'), 'text/csv'


registerAdapter(ReportRenderer, IReport, IAthenaRenderable)
