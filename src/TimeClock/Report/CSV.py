from TimeClock.Util.subclass import Subclass
from axiom.item import Item
from twisted.python.components import registerAdapter
from zope.interface import implementer


from ..Utils import coerce
from ..ITimeClock.IReport.IFormat import IFormat
from ..ITimeClock.IReport.IReportData import IReportData


@implementer(IFormat)
class CSV(object):
    name = "csv"
    def __init__(self, other=None):
        self.other=other
    @coerce
    def formatRow(self, row: IReportData) -> bytes:
        return (','.join(str(row[i[0]]) for i in self.table.getSchema())).encode('charmap') + b'\n'

    @coerce
    def formatHeader(self, table: Subclass[Item]) -> bytes:
        self.table=table
        return (','.join(i[0] for i in table.getSchema())).encode('charmap')+b'\n'
    @coerce
    def formatFooter(self, table: Subclass[Item]) -> bytes:
        return b''


registerAdapter(CSV, CSV, IFormat)
