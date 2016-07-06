from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database import Commands
from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ViewEmployees(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    subaccounts = None
    name = 'View Employees'
    def render_genericCommand(self, ctx: WovenContext, data):
        l = List(list(Store.query(Employee)), ['', "Employee ID", "Name"])
        l.closeable = False
        l.addRow(SaveList(3, start=1))
        l.prepare(self)
        l.visible = True
        return l


registerAdapter(ViewEmployees, Commands.ViewEmployees.ViewEmployees, IAthenaRenderable)
