import warnings

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from nevow import inevow
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IListRow)
class StaticListRow(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + '/Pages/List.xml', 'listRow')
    jsClass = 'TimeClock.Widgets.StaticListRow'
    @coerce
    def __init__(self, slots: list):
        super().__init__()
        for slot in slots:
            if IAthenaRenderable(slot, None):
                warnings.warn("StaticListRow should only be used for static content, not IAthenaRenderables")
                IAthenaRenderable(slot).prepare(self)
        self.slots = slots
    def render_listRow(self, ctx: WovenContext, data):
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        o = []
        for idx, slot in enumerate(self.slots):
            o.append(listCell(data=dict(listItem=slot, index=idx)))
        ctx.fillSlots('searchclass', 'self.searchClass')
        return o
    @property
    def length(self):
        return len(self.slots)

registerAdapter(StaticListRow, list, IListRow)
registerAdapter(StaticListRow, tuple, IListRow)
