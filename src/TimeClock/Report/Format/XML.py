from zope.component import provideUtility

from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from zope.interface import implementer, provider

from TimeClock.Utils import coerce
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData
from nevow import tags
from nevow import flat
from html5print import HTMLBeautifier


@implementer(IFormat)
@provider(IFormatterFactory)
class XML(object):
    name = "xml"
    columns = None
    def __init__(self, other=None):
        self.other = other
        self.header = tags.thead()
        self.body = tags.tbody()
        self.tag = tags.table()[self.header, self.body]

    @coerce
    def formatRow(self, row: IReportData) -> bytes:
        tr = tags.tr()[
            [tags.td()[row[i]] for i in self.columns]
        ]
        self.body.children.append(tr)
        return flat.flatten(tr)

    @coerce
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

    def getReport(self) -> bytes:
        return HTMLBeautifier.beautify(flat.flatten(self.tag).decode('charmap')).encode('charmap')


provideUtility(XML, IFormatterFactory, 'xls')
provideUtility(XML, IFormatterFactory, 'xml')
