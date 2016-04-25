from decimal import Decimal
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ITask import ITask
from TimeClock.ITimeClock.IReport.IReport import IReport
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Report.DynamicReport import DynamicReport
from TimeClock.Report.Format.CSV import CSV
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from nevow.athena import expose
from nevow.loaders import xmlfile
from .Editor import Editor


@implementer(IAthenaRenderable)
class TaskRennderer(AbstractRenderer):
    jsClass = "TimeClock.Tasks"
    docFactory = xmlfile(path + '/Pages/TaskRenderer.xml', 'TaskRendererPattern')

    def __init__(self, task: ITask):
        self.task = task
    def render_taskName(self, *a):
        return self.task.name
    def render_taskDescription(self, *a):
        return self.task.description
    def render_taskHours(self, *a):
        return str(self.task.expected_hours)
    @expose
    def viewDetails(self):
        e = Editor(self.task, 'description')
        e.prepare(self)
        e.visible = True
        return e, self.task.name, str(self.task.expected_hours)
    @expose
    def save(self, name, hours):
        self.task.name = name
        self.task.expected_hours = Decimal(hours)


registerAdapter(TaskRennderer, ITask, IAthenaRenderable)
