from unittest import TestCase

from twisted.python.components import registerAdapter

from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import coerce
from axiom.item import Item
from zope.interface import implementer, provider

from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.ITimeClock.IReport.IReportData import IReportData
from axiom.store import Store

from TimeClock.Database.Area import Area
from TimeClock.Database.Employee import Employee

from TimeClock.Report.SimpleReport import SimpleReport

s = Store()

Area(name='a1', store=s)
Area(name='a2', store=s)

Employee(store=s,
         emergency_contact_name = "John Doe",
         emergency_contact_phone = "509-xxx-xxxx",
         active_directory_name = 'jane.doe',
         employee_id = 1,
         alternate_authentication = None,
         supervisor = None)

Employee(store=s,
         emergency_contact_name="Jane Doe",
         emergency_contact_phone="509-xxx-xxxx",
         active_directory_name='john.doe',
         employee_id=2,
         alternate_authentication=None,
         supervisor=None)

sr1 = SimpleReport(store=s, name='test report', tableName='Area', description = 'test report 1')
sr2 = SimpleReport(store=s, name='test report', tableName='Area', description = 'test report 2', columns=['a2'], filters=['name'])

sr3 = SimpleReport(store=s, name='test report', tableName='Employee', description = 'test report 3')

@provider(IFormat)
class SimpleFormat(object):
    name = 'Simple Format'
    @staticmethod
    @coerce
    def formatRow(row: IReportData) -> bytes:
        return repr(list(row)).encode('charmap')
    @staticmethod
    @coerce
    def formatHeader(Type: Subclass[Item]) -> bytes:
        return b''
    @staticmethod
    @coerce
    def formatFooter(Type: Subclass[Item]) -> bytes:
        return b''


@implementer(IReportData)
class ReportData(object):
    def __init__(self, other):
        self.other=other
    def __getitem__(self, value):
        return getattr(self.other, value)
    @coerce
    def getValues(self) -> [object]:
        return list(self.other.persistentValues().values())
    def getColumns(self) -> [str]:
        return list(self.other.persistentValues().keys())
    def __iter__(self) -> [tuple]:
        return iter(self.other.persistentValues().items())


registerAdapter(ReportData, Item, IReportData)


class ReportTester(TestCase):
    def test_simpleReport(self):
        self.assertEqual(sr1.runReport(SimpleFormat), b"[('sub', None), ('name', 'a1')][('sub', None), ('name', 'a2')]")
        self.assertEqual(sr2.runReport(SimpleFormat), b"[('sub', None), ('name', 'a2')]")
    def testCSV(self):
        from TimeClock.Report.CSV import CSV
        print(sr3.runReport(CSV()).decode('charmap'))

