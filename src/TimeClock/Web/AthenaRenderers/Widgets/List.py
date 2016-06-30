from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce, overload
from TimeClock.Web.AthenaRenderers.Abstract.AbstractExpandable import AbstractExpandable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Objects.EmployeeRenderer import EmployeeRenderer
from nevow import inevow
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from . import StaticListRow


class List(AbstractRenderer, AbstractExpandable, AbstractHideable):
    jsClass = 'TimeClock.Widgets.List'
    cssClass = 'TimeClock.ListWidget'
    docFactory = xmlfile(path + '/Pages/List.xml', 'ListPattern')
    cols = None
    list = None
    selectable = False
    rendered = False

    limit = -1;

    # Setup
    @overload
    def __init__(self):
        super().__init__()
        self.list = []
    @overload
    def __init__(self, items, columns):
        self.__init__()
        self.setColumns(*columns)
        for i in items:
            self.addRow(i)
    @overload
    def __init__(self, items: [IListRow], *columns: [str]):
        self.__init__()
        self.setColumns(*columns)
        for i in items:
            self.addRow(i)

    def setColumns(self, *cols):
        self.cols = cols

    @coerce
    def addRow(self, row: IListRow):
        if self.cols is None:
            raise RuntimeError("Columns must be speicified before rows may be added")
        if row.length != len(self.cols):
            raise TypeError("Row of length %i expected, got %i" % (len(self.cols), row.length))
        self.list.append(row)
        row.prepare(self)
        if self.rendered:
            self.callRemote("append", row)

    def removeRow(self, item):
        for i in self.list:
            if isinstance(i, EmployeeRenderer) and i.getEmployee() is item:
                self.callRemote('remove', i._athenaID)
                self.list.remove(i)
                return

    def getInitialArguments(self):
        return (self.limit, )

    def setSelectable(self, b):
        self.selectable = b

    def setLimit(self, l):
        self.limit = l

    # Data Functions

    def data_tableHeader(self, ctx: WovenContext, data):
        ctx.fillSlots('tableTitle', self.name)
        tw = len(self.cols)
        ctx.fillSlots('titleWidth', tw)

    # Render Functions

    def render_header(self, ctx: WovenContext, data):
        headerRow = inevow.IQ(ctx).patternGenerator("headerRow")
        return (headerRow(data=dict(header=self.cols)))

    def render_headerRow(self, ctx: WovenContext, data):
        headerCell = inevow.IQ(ctx).patternGenerator("headerCell")
        o = []
        for c in data['header']:
            o.append(headerCell(data=dict(listHeader=c)))
        return o

    def render_list(self, ctx: WovenContext, data):
        self.rendered = True
        return self.list

    def render_selectable(self, ctx: WovenContext, data):
        return self.selectable


    # Remote Functions

