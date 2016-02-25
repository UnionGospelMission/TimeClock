from TimeClock.Util.subclass import Subclass
from axiom.item import Item
from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IReport.IReportData import IReportData


class IFormat(Interface):
    name = Attribute("name")
    def formatRow(row: IReportData) -> bytes:
        pass
    def formatHeader(table: Subclass[Item]) -> bytes:
        pass
    def formatFooter(table: Subclass[Item]) -> bytes:
        pass
