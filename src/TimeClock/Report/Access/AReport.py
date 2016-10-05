from zope.interface import implementer

from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Report.IAccess.IAEmployee import IAEmployee
from TimeClock.Report.IAccess.IAReport import IAReport
from TimeClock.Report.IAccess.IAReportData import IAReportData
from TimeClock.Utils import overload, coerce
from axiom.store import Store


@implementer(IAReport)
class AReport(object):
    def __init__(self, formatter: IFormat, store: Store):
        self._formatter = formatter
        self._store = store

    @coerce
    def getEmployees(self) -> [IAEmployee]:
        return self._store.query(Employee)

    @overload
    def formatRow(row: dict) -> bytes:
        pass
    @overload
    def formatRow(row: IAReportData) -> bytes:
        pass

    def formatHeader(columns: [str]) -> bytes:
        pass

    def formatFooter() -> bytes:
        pass
