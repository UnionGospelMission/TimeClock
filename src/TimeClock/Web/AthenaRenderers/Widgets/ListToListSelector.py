from TimeClock.Util.IterateInReactor import IterateInReactor
from twisted.internet import defer

from twisted.internet.defer import Deferred, succeed

from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.LiveFragment import LiveFragment
from nevow import inevow
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from . import StaticListRow


class ListToListSelector(AbstractRenderer, AbstractExpandable, AbstractHideable):
    jsClass = 'TimeClock.Widgets.ListToListSelector'
    docFactory = xmlfile(path + '/Pages/ListToList.xml', 'ListToListPattern')
    cols = None
    list = None
    element = None
    mappingReturnsNewElements = False

    # Setup
    @overload
    def __init__(self, l1: List, l2: List):
        super().__init__()
        self.l1 = l1
        self.l2 = l2

    def prepare(self, parent: LiveFragment):
        super().prepare(parent)
        self.l1.prepare(self)
        self.l2.prepare(self)
        self.l1.visible = True
        self.l2.visible = True
        self.l1.closeable = False
        self.l2.closeable = False
        self.l1.setSelectable(True)
        self.l1.setLimit(1)
        self.l2.setSelectable(True)

    def render_list1(self, ctx, data):
        return self.l1

    def render_list2(self, ctx, data):
        return self.l2

    def getMappingFor(self, element):
        return []

    def setMappingFor(self, elements):
        print("Not setting mapping for %r -> %r" % (self.element, elements))

    @expose
    def targetChanged(self, ID):
        self.element = element = self.page.getWidget(ID)
        m = self.getMappingFor(element)
        if not isinstance(m, Deferred):
            m = defer.succeed(m)

        d = Deferred()

        m.addCallback(d.callback)

        d.addCallback(self._targetChanged)

        return d

    def _targetChanged(self, m):
        if self.mappingReturnsNewElements:
            #IterateInReactor(self._setMapping(m), delay=0.0)
            #return m, True
            return m, True
        o = []
        for i in m:
            if isinstance(i, LiveFragment):
                i = i._athenaID
            o.append(i)
        return o, self.mappingReturnsNewElements

    # def _setMapping(self, m):
    #     for i in m:
    #         self.l2.addRow(i)
    #         yield

    @expose
    def doSave(self, elements: [int]):
        self.setMappingFor(self.element, [self.page.getWidget(ID) for ID in elements])

