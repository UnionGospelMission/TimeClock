from TimeClock.Report.IAccess.IAEmployee import IAEmployee
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible
from TimeClock.Util import fromFunction
from TimeClock.Utils import overload


class IAReport(IAbstractAccessible):
    def iterEmployees() -> [IAEmployee]:
        pass

    @overload
    def formatRow(row: dict) -> bytes:
        pass
    @fromFunction
    @overload
    def formatRow(row: IAReportData) -> bytes:
        pass

    def formatHeader(columns: [str]) -> bytes:
        pass

    def formatFooter() -> bytes:
        pass
