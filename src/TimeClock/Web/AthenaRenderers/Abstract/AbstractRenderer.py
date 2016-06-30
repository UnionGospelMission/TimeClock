from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable

from TimeClock.Web.LiveFragment import LiveFragment
from TimeClock.Web.Utils import formatShortName
from nevow.context import WovenContext


path = __file__.rsplit('/', 3)[0]


@implementer(IAthenaRenderable)
class AbstractRenderer(LiveFragment):
    def powerUp(self, obj, iface):
        self.powerups[iface] = self.powerups.get(iface, [])
        self.powerups[iface].append(obj)
    parent = None
    visible = False
    name = 'No Name'
    _topLevel = False
    closeable = True
    def __init__(self, *args, **kw):
        super().__init__()
        self.args = args
        self.kw = kw
    def topLevel(self, b: bool=True):
        self._topLevel = b
        if b:
            self.closeable = False
    @property
    def employee(self):
        if self.parent:
            return self.parent.employee
    def prepare(self, parent: LiveFragment, force: bool=False):
        if self.parent:
            if force:
                self.page = parent.page
        else:
            self.parent = parent
            self.setFragmentParent(parent)
        for child in self.liveFragmentChildren:
            child.prepare(self, force)
        return self
    def render_name(self, ctx, data):
        return formatShortName(self.name)
    def render_title(self, ctx, data):
        return "Time Clock - %s" % self.name
    def render_topLevel(self, *args):
        return formatShortName(self.name) if self._topLevel else ""
    def getName(self):
        return self.name
    def render_closeable(self, ctx: WovenContext, data):
        if self.closeable:
            return ""
        return "display:none"


