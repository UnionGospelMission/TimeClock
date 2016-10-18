from zope.interface import implementer

from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Report.Access.AMap import AMap
from TimeClock.Report.Access.ATimeDelta import ATimeDelta
from TimeClock.Report.IAccess import IAMap
from TimeClock.Report.IAccess.IAEmployee import IAEmployee
from TimeClock.Report.IAccess.IAReport import IAReport
from TimeClock.Report.IAccess.IAReportData import IAReportData
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible
from TimeClock.Report.Log import Log
from TimeClock.Utils import overload, coerce, i_coerce
from axiom.store import Store
import io


@implementer(IAReport)
class AReport(object):
    __slots__ = ['_formatter', '_store', '_log', '_interfaces']

    @coerce
    def __init__(self, formatter: IFormat, store: Store, log: Log, interfaces):
        self._formatter = formatter
        self._store = store
        self._log = log
        self._interfaces = tuple(interfaces)

    @property
    def formatterName(self):
        return self._formatter.name

    @i_coerce
    def getEmployees(self) -> IAEmployee:
        return self._store.query(Employee)

    @coerce
    def countEmployees(self) -> int:
        return self._store.query(Employee).count()

    @overload
    def formatRow(self, row: dict) -> bytes:
        return self._formatter.formatRow(row)

    @overload
    def formatRow(self, row: IAReportData) -> bytes:
        return self._formatter.formatRow(row)

    @overload
    def formatRow(self, row: AMap) -> bytes:
        return self._formatter.formatRow(row.copy())

    def formatHeader(self, columns: [str]) -> bytes:
        return self._formatter.formatHeader(columns)

    def formatFooter(self) -> bytes:
        return self._formatter.formatFooter()

    def getReport(self) -> bytes:
        return self._formatter.getReport()

    def log(self, level, obj):
        self._log.log(level, obj)

    def progress(self, progress):
        self._log.progress(progress)

    def getInterfaces(self) -> [IAbstractAccessible]:
        return self._interfaces

    def timeDelta(self, **kw):
        return ATimeDelta(**kw)

    def print(self, *args, **kw):
        i = io.StringIO()
        if 'file' in kw:
            kw.pop('file')
        print(*args, file=i, **kw)
        self.log('PRINT', i.getvalue().strip())

