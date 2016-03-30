from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from nevow.athena import expose
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ConfirmationRenderer(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/ConfirmationRenderer.xml", 'ConfirmationPattern')
    jsClass = "TimeClock.Confirmation"
    message = None
    data = None
    visible = True
    def __init__(self, cb, *args):
        self.cb = cb
        self.args = args
    def prepare(self, *args):
        super().prepare(*args)
        self.visible = True
    def setMessage(self, msg):
        self.message = msg
    def setData(self, dta):
        dta = IAthenaRenderable(dta, dta)
        if hasattr(dta, 'visible'):
            dta.visible = True
        self.data = dta
    def render_confirmationMsg(self, *args):
        return self.message
    def render_confirmationData(self, *args):
        return self.data
    @expose
    def confirm(self):
        return self.cb(*self.args)
