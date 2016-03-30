from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from nevow.athena import expose

from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from nevow.tags import select, option
from nevow.loaders import xmlfile
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.Commands.ClockIn import ClockIn
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path


@implementer(IAthenaRenderable)
class ClockInRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/ActionItem.xml", 'ActionItemPattern')
    def render_formArguments(self, ctx, idata):
        s = select(name="sub")
        se = ISolomonEmployee(self.employee)
        for a in self.employee.powerupsFor(ISubAccount):
            o = option(value=a.sub)[a.name]
            if se.defaultSubAccount == a:
                o(selected='')
            _ = s[o]
        w = select(name='wloc')
        for b in self.employee.getWorkLocations():
            o = option(value=b.workLocationID)[b.description]
            if se.defaultWorkLocation == b:
                o(selected='')
            _ = w[o]
        return [s, w]
    def render_actionName(self, ctx, idata):
        return "Clock In"
    @expose
    def runCommand(self, args):
        super(ClockInRenderer, self).runCommand(args)
        self.hide()
        self.parent.elements['clockOut'].show()
        self.parent.selectedElement = self.parent.elements['clockOut']
        if hasattr(self.parent, 'menu'):
            self.parent.parent.menu.hideClockIn()


registerAdapter(ClockInRenderer, ClockIn, IAthenaRenderable)
