import time

from twisted.internet import reactor

from TimeClock.Web.Favicon import Favicon
from nevow import rend, inevow, static
from zope.interface import implementer

from nevow.athena import LivePage, MappingResource, _collectPackageBelow
from ..ITimeClock.IWeb.IAthena import IAthenaJS
from .TimeClockPage import TimeClockPage, path
from TimeClock.Web.LoginPage import LoginPage


@implementer(IAthenaJS)
class AthenaJS(object):
    AthenaHandler = None
    LP = LivePage()
    class AthenaPage(rend.Page):
        def renderHTTP(self, ctx):
            if ctx.arg(b"pageId", b'').decode('charmap') in TimeClockPage.pages:
                return TimeClockPage.pages.pop(ctx.arg(b"pageId", b'').decode('charmap'))

            return LoginPage()

        def locateChild(self, ctx, segments):
            images = _collectPackageBelow(path + '/Images', 'png')
            if segments and segments[0].startswith('favicon'):
                return Favicon(), ()
            if segments and segments[0] == 'images':
                img = str.join('.', segments[1:]).split('.png')[0]
                if img in images:
                    return [static.File(images[img]), []]

            if segments == ['']:
                return self, ()
            return AthenaJS.LP.locateChild(ctx, segments)
        @staticmethod
        def cleanup():
            for k, p in TimeClockPage.pages.copy().items():
                if time.time() - p.creationTime > 300:
                    TimeClockPage.pages.pop(k)
            reactor.callLater(300, AthenaJS.AthenaPage.cleanup)

    jsDeps = {}
    Ports = (('TCP', 8080),)


reactor.callLater(300, AthenaJS.AthenaPage.cleanup)
