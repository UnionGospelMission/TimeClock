from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from nevow.athena import expose

from TimeClock.Database.Commands.ClockOut import ClockOut
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
class ClockOutRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/ActionItem.xml", 'ActionItemPattern')
    def render_formArguments(self, ctx, idata):
        return []
    def render_actionName(self, ctx, idata):
        return "Clock Out"
    @expose
    def runCommand(self, args):
        super(ClockOutRenderer, self).runCommand(args)
        self.hide()
        self.parent.elements['clockIn'].show()
        self.parent.selectedElement = self.parent.elements['clockIn']
        if hasattr(self.parent, 'menu'):
            self.parent.menu.hideClockOut()
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'menu'):
            self.parent.parent.menu.hideClockOut()



registerAdapter(ClockOutRenderer, ClockOut, IAthenaRenderable)
