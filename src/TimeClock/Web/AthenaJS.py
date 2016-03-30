from nevow import rend, inevow
from zope.interface import implementer

from ..ITimeClock.IWeb.IAthena import IAthenaJS
from .TimeClockPage import TimeClockPage
from TimeClock.Web.LoginPage import LoginPage

@implementer(IAthenaJS)
class AthenaJS(object):
    AthenaHandler = None
    class AthenaPage(rend.Page):
        def renderHTTP(self, ctx):
            if ctx.arg(b"pageId", b'').decode('charmap') in TimeClockPage.pages:
                print(15, "logged in")
                return TimeClockPage.pages.pop(ctx.arg(b"pageId", b'').decode('charmap'))

            return LoginPage()
        def locateChild(self, ctx, segments):
            if segments == ['']:
                return self, ()
            return TimeClockPage(None).locateChild(ctx, segments)

    jsDeps = {}
    Ports = (('TCP', 8080),)



