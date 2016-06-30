from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaHideable import IAthenaHideable
from TimeClock.Web.LiveFragment import LiveFragment


@implementer(IAthenaHideable)
class AbstractHideable(object):
    visible = True

    def hide(self):
        self.visible = False
        self.callRemote("hide");
    def show(self):
        self.visible = True
        self.callRemote("show");
    def render_visibility(self, ctx, idata):
        if self.visible:
            return "display:block"
        return "display:none"
