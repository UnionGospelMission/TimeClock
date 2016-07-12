from twisted.python.components import registerAdapter
from zope.component import provideUtility

from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from axiom.item import Item
from zope.interface import implementer, provider

from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData
from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import coerce
import json


@implementer(IFormat)
@provider(IFormatterFactory)
class JSON(object):
    name = "json"
    def __init__(self, other=None):
        self.other = other
        self.columns = None
        self.first = False
        self.last = False
        self.rows = []
        self.functions = []
    @coerce
    def formatRow(self, row: IReportData) -> bytes:
        if self.first:
            ret = '\n    '
            self.first = False
        else:
            ret = ',\n    '
        self.rows.append((ret + json.dumps({k: row[k] for k in self.columns})).encode('charmap'))
        return self.rows[-1]

    @coerce
    def formatHeader(self, columns: [str]) -> bytes:
        self.columns = columns
        self.first = True
        self.rows.append(b'[')
        return b'['
    @coerce
    def formatFooter(self) -> bytes:
        self.rows.append(b'\n]')
        self.last = True
        return b'\n]'

    def getReport(self) -> bytes:
        if not self.last:
            self.formatFooter()
        return bytes.join(b'', self.rows)

provideUtility(JSON, IFormatterFactory, 'json')
