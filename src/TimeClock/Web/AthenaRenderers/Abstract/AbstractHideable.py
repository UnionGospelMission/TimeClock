from twisted.internet import reactor
from twisted.internet.defer import Deferred
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaHideable import IAthenaHideable
from TimeClock.Web.LiveFragment import LiveFragment


@implementer(IAthenaHideable)
class AbstractHideable(object):
    visible = True

    def hide(self):
        self.visible = False
        self.callRemote("hide")

    def show(self):
        self.visible = True
        self.callRemote("show")

    def render_visibility(self, ctx, idata):
        if self.visible:
            ret = "display:block"
        else:
            ret = "display:none"
        return ret
