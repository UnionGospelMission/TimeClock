from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData
from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import coerce
import json


@implementer(IFormat)
class JSON(object):
    name = "json"
    def __init__(self, other=None):
        self.other = other
        self.table = None
        self.first = False
    @coerce
    def formatRow(self, row: IReportData) -> bytes:
        if self.first:
            ret = '\n    '
            self.first = False
        else:
            ret = ',\n    '
        return json.encode(row.persistentValues()).encode('charmap')

    @coerce
    def formatHeader(self, table: Subclass[Item]) -> bytes:
        self.table = table
        self.first = True
        return b'['
        # return (','.join(i[0] for i in table.getSchema())).encode('charmap')+b'\n'
    @coerce
    def formatFooter(self, table: Subclass[Item]) -> bytes:
        return b']'

