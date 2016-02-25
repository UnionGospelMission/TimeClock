from axiom.attributes import text, textlist, AND
from axiom.item import Item

from zope.interface import implementer

from ..ITimeClock.IReport.IReport import IReport
from ..ITimeClock.IReport.IFormat import IFormat
from ..Database import tables


@implementer(IReport)
class SimpleReport(Item):
    name = text()
    tableName = text()
    columns = textlist()
    filters = textlist()
    description = text()

    def runReport(self, format: IFormat) -> bytes:
        out = []
        table = tables[self.tableName]
        out.append(format.formatHeader(table))
        if self.columns:
            filter_ = getattr(table, self.filters[0]) == self.columns[0]
            for idx, c in enumerate(self.columns[1:]):
                filter_ = AND(filter_, getattr(table, self.filters[idx]) == c)
        else:
            filter_ = None
        result = self.store.query(table, filter_)
        for row in result:
            out.append(format.formatRow(row))
        out.append(format.formatFooter(table))
        return bytes.join(b'', out)

    def getDescription(self) -> str:
        return 'SimpleReport for %s filtered by %s\n\n%s'%(
            self.tableName,
            ', '.join(self.columns),
            self.description
        )
