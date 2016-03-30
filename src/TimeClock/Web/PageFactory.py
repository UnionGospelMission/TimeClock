from nevow.athena import jsDeps

from TimeClock.ITimeClock.IWeb.IAthena import IAthenaJS
from nevow import inevow
from zope.interface import implementer


@implementer(inevow.IResource)
class PageFactory(object):
    def __init__(self, iajs, port=None):
        self.iajs_module=iajs
        self.iajs=None
        v = vars(iajs)
        for attr in v:
            val=v[attr]
            # if IAthenaJS.providedBy(val):
            #     self.iajs = val
            #     break
            try:
                if IAthenaJS.implementedBy(val):
                    self.iajs = val
                    break
            except:
                continue
        if not self.iajs:
            raise RuntimeError("No implementer of IAthenaJS found in %r"%iajs)
        AthenaHandler=self.iajs.AthenaHandler
        if not hasattr(self.iajs.AthenaPage, "render_athenaHandler"):
            def render_athenaHandler(self, ctx):
                c = AthenaHandler()
                c.setFragmentParent(self)
                return c
            self.iajs.AthenaPage.render_athenaHandler=render_athenaHandler
        jsDeps.mapping.update(self.iajs.jsDeps)
        if port:
            self.iajs.Ports=(("TCP", int(port)),)
        self.AthenaPage=type("AthenaPage",(self.iajs.AthenaPage,),{})
        self.AthenaPage.renderHTTP=self.renderHTTP

    def renderHTTP(self, ctx):
        return self.iajs.AthenaPage()
    def locateChild(self, ctx, segments):
        if segments == ('',):
            return self, ()
        return self.iajs.AthenaPage().locateChild(ctx, segments)
