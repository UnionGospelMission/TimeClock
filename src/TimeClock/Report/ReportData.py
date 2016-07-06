from twisted.python.components import registerAdapter

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReportData import IReportData


@implementer(IReportData)
class ReportData(object):
    def __init__(self, data: Item):
        self.data = data
    def __getitem__(self, i):
        return str(self.data[i])

    def __iter__(self) -> [tuple]:
        return iter(self.data)

    @staticmethod
    def fromItem(item):
        return ReportData(item.persistentValues())


registerAdapter(ReportData, dict, IReportData)
registerAdapter(ReportData.fromItem, Item, IReportData)
