from TimeClock import Exceptions
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from . import Solomon
import time


@implementer(ISolomonEmployee)
class SolomonEmployee(object):
    __cache__ = {}

    @overload
    def __init__(self, employee_id: int):
        self.employee = IEmployee(employee_id)
        record = Solomon.getEmployee(str(employee_id))
        if not record:
            record = Solomon.dummyEntries[str(employee_id)]
            record['Name'] = 'Employee Missing'
        self.record = record

    @overload
    def __init__(self, employee: IEmployee):
        self.employee = employee
        record = Solomon.getEmployee(employee.employee_id)
        if not record:
            record = Solomon.dummyEntries[str(employee.employee_id)]
            record['Name'] = 'Employee Missing'
        self.record = record

    @overload
    def __init__(self, employee: IEmployee, record: dict):
        self.employee = employee
        self.record = record

    @classmethod
    def fromIEmployee(cls, employee: IEmployee):
        cached = cls.__cache__.get(employee)
        if not cached or cached[1] < time.time():
            ise = cls(employee)
            cls.__cache__[employee] = [ise, time.time()+600]
            return ise
        return cached[0]

    @classmethod
    def fromInt(cls, eid: int):
        return cls.fromIEmployee(IEmployee(eid))

    @property
    @coerce
    def defaultSubAccount(self) -> ISubAccount:
        if not Solomon.pymssql:
            wl = self.employee.getSubAccounts()
            if not wl:
                raise Exceptions.DatabasException("Solomon unavailable and no cached sub account")
            return wl[0]
        else:
            area = ISubAccount(int(self.dfltExpSub), None)
        if not area:
            area = ISubAccount(NULL)
            s_area = Solomon.getSubAccount(self.dfltExpSub)
            area.name = s_area['Descr'].strip()
            area.sub = int(self.dfltExpSub)
        return area

    @property
    @coerce
    def defaultWorkLocation(self) -> IWorkLocation:
        if not Solomon.pymssql:
            wl = self.employee.getWorkLocations()
            if not wl:
                raise Exceptions.DatabasException("Solomon unavailable and no cached work location")
            return wl[0]
        else:
            wl = IWorkLocation(self.dfltWrkloc, None)
        if not wl:
            wl = IWorkLocation(NULL)
            wl.workLocationID = self.dfltWrkloc
            wl.description = Solomon.getWorkLocation(self.dfltWrkloc)['Descr'].strip()
        return wl

    def __getattr__(self, item):
        for i in self.record:
            if i[0].lower() + i[1:] == item:
                if isinstance(self.record[i], str):
                    return self.record[i].strip()
                return self.record[i]
        return object.__getattribute__(self, item)

    @coerce
    def getBenefits(self) -> [IBenefit]:
        return Solomon.getBenefits(self.employee)

    def getAvailableBenefits(self) -> dict:
        return {i: Solomon.getBenefitAvailable(i) for i in self.getBenefits()}

    @property
    def stdSlry(self):
        if 'StdSlry' in self.record:
            return self.record['StdSlry']
        return 0


registerAdapter(SolomonEmployee.fromIEmployee, IEmployee, ISolomonEmployee)
registerAdapter(SolomonEmployee.fromInt, int, ISolomonEmployee)

