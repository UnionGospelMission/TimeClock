from collections import OrderedDict
from collections.abc import Iterable

from twisted.python.components import registerAdapter

from TimeClock.ITimeClock.IFiniteSequence import IFiniteSequence
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Utils import coerce, overload
from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from nevow.stan import Tag
from .AbstractRenderer import AbstractRenderer, path


class ListRenderer(AbstractRenderer):
    selectable = True
    docFactory = xmlfile(path + '/Pages/List.xml', 'ListPattern')
    jsClass = "TimeClock.ListRenderer"
    initialArgs = ()
    limit = -1
    itemsVisible = False
    @overload
    def __init__(self, lst: IFiniteSequence, title=None, limit=-1):
        self.list = lst
        self.callback = None
        self.name = title or "List"
        self.limit = limit
    @overload
    def __init__(self, lst: Iterable, title=None):
        self.list = list(lst)
        self.callback = None
        self.name = title or "List"
    def prepare(self, parent, callback=None, title=None):
        super().prepare(parent)
        if title is None:
            title = self.name
        for idx, i in enumerate(self.list):
            if IAthenaRenderable(i, None):
                i = self.list[idx] = IAthenaRenderable(i)
                i.prepare(self)
                if self.itemsVisible is True:
                    i.visible = True
                elif self.itemsVisible is False:
                    i.visible = False
            elif isinstance(i, dict):
                for k, v in i.items():
                    if IAthenaRenderable(v, None):
                        v = i[k] = IAthenaRenderable(v)
                        v.prepare(self)
                        if self.itemsVisible is True:
                            v.visible = True
                        elif self.itemsVisible is False:
                            v.visible = False
        self.callback = callback
        self.name = title
    def data_tableHeader(self, ctx, data):
        ctx.fillSlots('tableTitle', self.name)
        tw = 0
        if self.list and isinstance(self.list[0], dict):
            tw = len(self.list[0])
        ctx.fillSlots('titleWidth', tw)

    def render_list(self, ctx: WovenContext, data):
        listRow = inevow.IQ(ctx).patternGenerator("listRow")
        o = []
        for idx, i in enumerate(self.list):
            o.append(listRow(data=dict(index=idx, listItem=i)))
        return o
    def render_header(self, ctx: WovenContext, data):
        headerRow = inevow.IQ(ctx).patternGenerator("headerRow")
        if self.list and isinstance(self.list[0], dict):
            return (headerRow(data=dict(header=self.list[0].keys())))
        return ""
    def render_headerRow(self, ctx: WovenContext, data):
        headerCell = inevow.IQ(ctx).patternGenerator("headerCell")
        o = []
        for c in data['header']:
            o.append(headerCell(data=dict(listHeader=c)))
        return o
    def render_listRow(self, ctx: WovenContext, data):
        listCell = inevow.IQ(ctx).patternGenerator("listCell")
        o = []
        if isinstance(data['listItem'], dict):
            for i, v in data['listItem'].items():
                o.append(listCell(data=dict(searchclass=i, index=data['index'], listItem=v)))
            return o
        ctx.fillSlots('searchclass', self.name)
        return listCell(data=data)
    @expose
    def itemDblClicked(self, idx: int):
        idx = int(idx)
        if callable(self.callback):
            return self.callback(idx)
    def render_selectable(self, *_):
        if self.selectable:
            return "true"
        return ""
    def getInitialArguments(self):
        return [self.limit]

registerAdapter(ListRenderer, list, IAthenaRenderable)


