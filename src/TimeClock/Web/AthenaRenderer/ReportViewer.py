from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.Commands.ViewReports import ViewReports
from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Report.DynamicReport import DynamicReport
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderer.Editor import Editor
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from TimeClock.Axiom.Store import Store
from nevow import tags as t
from nevow import tags as t


exampleCode = '''(('var1', 'int'), ('var2', 'float'))


formatHeader(["Hello", "World"])
formatRow({"Hello": "Hola", "World":"Mundo"})
'''


@implementer(IAthenaRenderable)
class ReportViewer(AbstractRenderer):
    rv = None
    jsClass = "TimeClock.Reports"
    docFactory = xmlfile(path + '/Pages/ReportViewer.xml', 'ReportViewerPattern')
    name = 'View Reports'
    newReport = None
    nrEditor = None

    @expose
    def listReports(self):
        reports = Store.powerupsFor(IReport)
        self.rv = ListRenderer([{'Name': i.name, 'Description': i.description, '': i} for i in reports])
        self.rv.itemsVisible = True
        self.rv.prepare(self, 'Reports')
        self.rv.visible = True
        self.rv.limit = 0
        self.rv.selectable = False
        return self.rv
    @expose
    def showEditor(self):
        self.nrEditor.show()



    def onSave(self):
        self.callRemote("getNameAndDescr")
    @expose
    def setNameAndDescr(self, name, descr):
        self.newReport.name = name
        self.newReport.description = descr
        self.newReport.store = Store
        Store.powerUp(self.newReport, IReport)
        self.newReport = DynamicReport(code=exampleCode)
        self.nrEditor.obj = self.newReport
    def render_listReports(self, ctx: WovenContext, data):

        ret = [t.input(type='button', value="View Reports")[
                   t.Tag('athena:handler')(handler='listReports', event='onclick')],
               t.input(type='button', id='refresh', value='Refresh', style='display:none')[
                   t.Tag('athena:handler')(handler='refreshReports', event='onclick')]]
        for p in self.preprocessors:
            ret = p(ret)
        return ret
    def render_createReport(self, ctx: WovenContext, data):
        self.newReport = DynamicReport(code=exampleCode)
        self.nrEditor = Editor(self.newReport, 'code')
        self.nrEditor.prepare(self)
        ret = [
            t.input(id='newReport', type='button', value='New Report')[
                t.Tag("athena:handler")(event="onclick", handler="newReport")],
            t.input(id="newReportName", style='display:none'),
            t.textarea(id="newReportDescription", style='display:none'),
            self.nrEditor
        ]
        self.nrEditor.visible = False;
        for p in self.preprocessors:
            ret = p(ret)
        return ret

registerAdapter(ReportViewer, ViewReports, IAthenaRenderable)
