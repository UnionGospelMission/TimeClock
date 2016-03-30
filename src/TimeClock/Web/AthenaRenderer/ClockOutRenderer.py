from TimeClock.ITimeClock.IDatabase.IArea import IArea
from nevow.tags import select, option
from nevow.loaders import xmlfile
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.Commands.ClockIn import ClockIn
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path


@implementer(IAthenaRenderable)
class ClockInRenderer(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/ClockIn.xml", 'ActionItemPattern')
    jsClass = "CommandRenderer.Commands"
    def __init__(self, command: ICommand):
        self.command = command
    def render_formArguments(self, ctx, idata):
        s = select(name="area")
        for a in self.employee.powerupsFor(IArea):
            s[option(id=a.sub)[a.name]]
        return s


registerAdapter(ClockInRenderer, ClockIn, IAthenaRenderable)
