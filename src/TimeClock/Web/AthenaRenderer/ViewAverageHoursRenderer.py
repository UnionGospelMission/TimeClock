from TimeClock.Database.Commands.ViewHours import ViewHours
from TimeClock.Util.DateTime import DateTime
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.Calendar import Calendar
from nevow.athena import expose

from nevow.loaders import xmlfile
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from nevow.tags import input


@implementer(IAthenaRenderable)
class ViewHoursRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/ActionItem.xml", 'ActionItemPattern')
    jsClass = "ViewHoursRenderer.ViewHours"
    def render_formArguments(self, ctx, idata):
        return [input(type="date", name="startDate"), input(type="date", name="endDate")]
    def render_actionName(self, ctx, idata):
        return "View Hours"
    @expose
    def runCommand(self, args):
        a = []
        for i in args:
            a.append(DateTime.get(i))
        print(29, a)
        iar = IAthenaRenderable(super(ViewHoursRenderer, self).execute(*a))
        iar.prepare(self)
        iar.visible = True
        iar.setStartDate(a[0])
        iar.setEndDate(a[1])
        return iar



registerAdapter(ViewHoursRenderer, ViewHours, IAthenaRenderable)
