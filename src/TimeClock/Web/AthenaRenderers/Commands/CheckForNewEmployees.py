from twisted.python.components import registerAdapter

from TimeClock.Database import Commands
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


class CheckForNewEmployees(AbstractRenderer):
    name = 'Check For New Employees'
    jsClass = 'TimeClock.Commands.CheckForNewEmployees'
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    def render_visibility(self, *a):
        return 'display:none'
    def render_class(self, *a):
        return 'CheckForNewEmployees'
    def render_genericCommand(self, ctx: WovenContext, data):
        button = tags.input(type='button', value='Check For New Employees')[tags.Tag('athena:handler')(handler='runCheck', event='onclick')]
        return self.preprocess([button])

    @expose
    def runCheck(self):
        if IAdministrator(self.employee, None):
            l1 = List(list(self.args[0].execute(self.employee)), ["", "Employee ID", "Name"])
            l1.prepare(self)
            l1.visible = True
            l1.selectable = False
            l1.addRow(SaveList(3, start=1))
            return l1

registerAdapter(CheckForNewEmployees, Commands.CheckForNewEmployees.CheckForNewEmployees, IAthenaRenderable)
