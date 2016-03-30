from TimeClock.Database.Commands.ViewAverageHours import ViewAverageHours
from TimeClock.Web.AthenaRenderer.ViewHoursRenderer import ViewHoursRenderer
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable


@implementer(IAthenaRenderable)
class ViewAverageHoursRenderer(ViewHoursRenderer):
    pass


registerAdapter(ViewAverageHoursRenderer, ViewAverageHours, IAthenaRenderable)
