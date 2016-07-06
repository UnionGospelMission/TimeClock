from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from nevow import inevow, tags
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IListRow)
class SaveList(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + '/Pages/List.xml', 'liveListRow')
    jsClass = 'TimeClock.Widgets.SaveList'
    length = 2
    @coerce
    def __init__(self, length=2, start=0):
        if length < 1:
            raise TypeError("Save Button Row length must be at least 1")
        super().__init__()
        self.length = length
        self.start = start
    def render_searchclass(self, ctx: WovenContext, data):
        return 'save'
    def render_listRow(self, ctx: WovenContext, data):
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        ctx.fillSlots('searchclass', 'self.searchClass')
        save = self.preprocess([tags.input(id='saveList', type='button', value='Save')[tags.Tag('athena:handler')(event='onclick', handler='saveAll')]])
        if self.length == 1:
            return listCell(data=dict(listItem=save, index=0))
        o = []
        for i in range(self.start):
            o.append(listCell(data=dict(listItem='', index=i)))
        o.extend([listCell(data=dict(listItem="Save Changes", index=0)),
                  listCell(data=dict(listItem=save, index=self.start))])
        for idx in range(self.length - 2 - self.start):
            o.append(listCell(data=dict(listItem='', index=idx + 2 + self.start)))

        return o


