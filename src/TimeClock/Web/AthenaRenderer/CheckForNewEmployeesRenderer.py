from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.Commands.CheckForNewEmployees import CheckForNewEmployees
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.ViewEmployeesRenderer import ViewEmployeesRenderer


@implementer(IAthenaRenderable)
class CheckForNewEmployeesRenderer(ViewEmployeesRenderer):
    def render_formArguments(self, ctx, idata):
        return []

registerAdapter(CheckForNewEmployeesRenderer, CheckForNewEmployees, IAthenaRenderable)
