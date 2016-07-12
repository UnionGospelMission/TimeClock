from zope.component import provideUtility

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from zope.interface import implementer, provider

from TimeClock.ITimeClock.IWeb.IListRow import IListRow
from TimeClock.Utils import coerce, overload
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer
from TimeClock.Web.LiveFragment import LiveFragment
from nevow import tags
from nevow import flat

from nevow.context import WovenContext
from nevow.loaders import xmlstr
from nevow.stan import Tag


@implementer(IFormat)
@provider(IFormatterFactory)
class ReportWidget(AbstractRenderer):
    name = "Widget"
    docFactory = xmlstr('''<div id="List" n:render="liveFragment" xmlns:athena="http://divmod.org/ns/athena/0.7" xmlns:n="http://nevow.com/ns/nevow/0.1"><invisible n:render="reportWidget"/></div>''')
    jsClass = 'TimeClock.Objects'
    columns = None
    selectable = False;
    cols = [1, 2, 3]
    def setStyle(self, tag, style):
        tag.attributes['style'] = style

    def __init__(self, other=None):
        super().__init__()
        self.other = other
        self.header = tags.thead()
        self.body = tags.tbody(border='1px solid black')
        self.tag = tags.table(border='1 px solid black')[self.header, self.body]
        self.functions = [self.setStyle]
    def render_reportWidget(self, ctx: WovenContext, data):
        return flat.flatten(self.preprocess(self.tag))

    @overload
    def formatRow(self, row: IReportData) -> bytes:
        tr = tags.tr(border='1px solid black')[
            [tags.td()[row[i]] for i in self.columns]
        ]
        self.body.children.append(tr)
        return flat.flatten(tr)

    @overload
    def formatRow(self, tag: Tag) -> bytes:
        self.body.children.append(tag)
        return b''

    @overload
    def formatRow(self, row: IEmployee) -> bytes:
        r = IListRow(row)
        r.prepare(self)
        r.length = 3
        self.body.children.append(r)
        return b''



    @overload
    def formatHeader(self, tag: Tag) -> bytes:
        self.header.children.append(tag)
        return b''
    @overload
    def formatHeader(self, columns: [str]) -> bytes:
        self.columns = columns
        tr = tags.tr()[
            [tags.th()[i] for i in self.columns]
        ]
        self.header.children.append(tr)
        return flat.flatten(tr)

    @coerce
    def formatFooter(self) -> bytes:
        return b''

    @overload
    def getReport(self):
        return self
    @overload
    def getReport(self) -> bytes:
        return b''


provideUtility(ReportWidget, IFormatterFactory, 'widget')
