from TimeClock.Database.Commands.ChangeAuthentication import ChangeAuthentication
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from nevow import tags
from nevow.athena import expose

from nevow.loaders import xmlfile
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path


@implementer(IAthenaRenderable)
class ChangePasswordRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + "/Pages/ActionItem.xml", 'ActionItemPattern')
    def render_formArguments(self, ctx, idata):
        return [tags.input(name="password", type="password")]
    @expose
    def runCommand(self, *a):
        self.hide()
        return super().runCommand(*a)


registerAdapter(ChangePasswordRenderer, ChangeAuthentication, IAthenaRenderable)
