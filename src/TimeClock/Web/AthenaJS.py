import time

from twisted.internet import reactor

from TimeClock.Web.Favicon import Favicon
from TimeClock.Web.TimeClockStationPage import TimeClockStationPage
from nevow import rend, inevow, static
from zope.interface import implementer

from nevow.athena import LivePage, MappingResource, _collectPackageBelow
from ..ITimeClock.IWeb.IAthena import IAthenaJS
from .TimeClockPage import TimeClockPage, path, getId
from TimeClock.Web.LoginPage import LoginPage
tcsCookies = []

@implementer(IAthenaJS)
class AthenaJS(object):
    AthenaHandler = None
    LP = LivePage()
    class AthenaPage(rend.Page):
        def renderHTTP(self, ctx):
            req = inevow.IRequest(ctx)
            cookies = req.received_cookies
            tcs = cookies.get(b'tcs', None)
            if tcs in tcsCookies:
                tcsCookies.remove(tcs)
                if cookies.get(b'lastPage', b'login') == b'tcs':
                    p = TimeClockStationPage()
                    cid = getId()
                    inevow.IRequest(ctx).setHeader('Set-Cookie', 'tcs=%s; Max-Age=604800' % cid)
                    tcsCookies.append(cid.encode('charmap'))
                    return p
            if ctx.arg(b"pageId", b'').decode('charmap') in TimeClockPage.pages:
                p = TimeClockPage.pages.pop(ctx.arg(b"pageId", b'').decode('charmap'))
                if isinstance(p, TimeClockStationPage):
                    cid = getId()
                    inevow.IRequest(ctx).setHeader('Set-Cookie', 'tcs=%s; Max-Age=2592000' % cid)
                    tcsCookies.append(cid.encode('charmap'))
                return p

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
