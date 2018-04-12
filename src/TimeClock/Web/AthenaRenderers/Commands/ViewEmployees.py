from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Solomon import Solomon
from TimeClock.Utils import coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ViewEmployees(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ViewEmployees'
    subaccounts = None
    name = 'View Employees'
    l = None
    loaded = False

    def render_class(self, *a):
        return "ViewEmployees"

    def render_genericCommand(self, ctx: WovenContext, data):
        self.l = l = List([], ['', "Employee ID", "Name"])
        l.closeable = False
        l.addRow(SaveList(3, start=1))
        l.prepare(self)
        l.visible = True
        showActive = tags.input(id='showActive', type='checkbox', checked=True)[
            tags.Tag('athena:handler')(handler='refresh', event='onchange')
        ]
        showInactive = tags.input(id='showInactive', type='checkbox')[
            tags.Tag('athena:handler')(handler='refresh', event='onchange')
        ]
        self.preprocess([showActive, showInactive])
        return "Show Active", showActive, tags.br(), "Show Inactive", showInactive, l

    @coerce
    def getEmployees(self, active, inactive) -> [IEmployee]:
        for i in Store.query(Employee):
            ise = ISolomonEmployee(i)
            if ise.status == Solomon.ACTIVE and active:
                yield i
            elif ise.status == Solomon.INACTIVE and inactive:
                yield i

    @expose
    def load(self, active: bool=True, inactive: bool=False):
        if not self.loaded:
            self.reload(active, inactive)
            self.loaded = True

    @expose
    def reload(self, active, inactive):
        self.l.list = [IListRow(i) for i in self.getEmployees(active, inactive)]
        for i in self.l.list:
            i.prepare(self.l)
            i.visible = True
        self.l.callRemote('select', self.l.list, True)


registerAdapter(ViewEmployees, Commands.ViewEmployees.ViewEmployees, IAthenaRenderable)
