from zope.component import provideUtility

from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from TimeClock.Util.subclass import Subclass
from axiom.item import Item
from twisted.python.components import registerAdapter
from zope.interface import implementer, provider

from TimeClock.Utils import coerce
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData


@implementer(IFormat)
@provider(IFormatterFactory)
class CSV(object):
    name = "csv"
    columns = None
    def __init__(self, other=None):
        self.other = other
        self.rows = []
        self.functions = []
    @coerce
    def formatRow(self, row: IReportData) -> bytes:
        self.rows.append(str.join(',', (row[i] for i in self.columns)).encode('charmap') + b'\n')
        return self.rows[-1]

    @coerce
    def formatHeader(self, columns: [str]) -> bytes:
        self.columns = columns
        self.rows.append((','.join(columns)).encode('charmap') + b'\n')
        return self.rows[-1]

    @coerce
    def formatFooter(self) -> bytes:
        return b''

    def getReport(self) -> bytes:
        return bytes.join(b'', self.rows)


provideUtility(CSV, IFormatterFactory, 'csv')
