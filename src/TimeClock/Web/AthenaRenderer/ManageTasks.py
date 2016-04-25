from decimal import Decimal
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.CreateTask import CreateTask
from TimeClock.Database.Task import Task
from TimeClock.ITimeClock.IDatabase.ITask import ITask
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Util import NULL
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderer.Editor import Editor
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow import tags as t


@implementer(IAthenaRenderable)
class ManageTasks(AbstractRenderer):
    docFactory = xmlfile(path + '/Pages/ManageTasks.xml', 'ManageTasksPattern')
    jsClass = 'TimeClock.Tasks'
    newTask = None
    ntEditor = None
    tv = None
    name = 'Manage Tasks'
    def render_listTasks(self, ctx: WovenContext, data):

        ret = [t.input(type='button', value="View Tasks")[
               t.Tag('athena:handler')(handler='listTasks', event='onclick')],
               t.input(type='button', id='refresh', value='Refresh', style='display:none')[
                   t.Tag('athena:handler')(handler='refreshTasks', event='onclick')]]
        for p in self.preprocessors:
            ret = p(ret)
        return ret
    def render_createTask(self, ctx: WovenContext, data):
        self.newTask = dict(description='')
        self.ntEditor = Editor(self.newTask, 'description', (lambda a, b: a[b]), (lambda a, b, c: a.__setitem__(b,c)))
        self.ntEditor.prepare(self)
        ret = [
            t.input(id='newTask', type='button', value='New Task')[t.Tag("athena:handler")(event="onclick", handler="newTask")],
            t.input(id="newTaskName", style='display:none', placeholder='Name'),
            t.input(id="newTaskHours", type='number', step='0.01', placeholder='Expected Hours', style='display:none'),
            self.ntEditor
        ]
        self.ntEditor.visible = False;
        for p in self.preprocessors:
            ret = p(ret)
        return ret
    @expose
    def showEditor(self):
        self.ntEditor.show()
    def onSave(self):
        self.callRemote("getNameAndHours")
    @expose
    def setNameAndHours(self, name, hours):
        nt = ITask(NULL)
        nt.name = name
        nt.expected_hours = Decimal(hours)
        nt.description = self.newTask['description']
        Store.powerUp(nt, ITask)
        self.newTask = {'description': ''}
        self.ntEditor.obj = self.newTask
    @expose
    def listTasks(self):
        reports = Store.powerupsFor(ITask)
        self.tv = ListRenderer([{'Name': i.name, 'Description': i.description, 'Hours': str(i.expected_hours), '': i}
                                for i in reports])
        self.tv.itemsVisible = True
        self.tv.prepare(self, 'Tasks')
        self.tv.visible = True
        self.tv.limit = 0
        self.tv.selectable = False
        return self.tv


registerAdapter(ManageTasks, CreateTask, IAthenaRenderable)
