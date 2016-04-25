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


@implementer(ISolomonEmployee)
class SolomonEmployee(object):
    @overload
    def __init__(self, employee_id: int):
        self.employee = IEmployee(employee_id)
        self.record = Solomon.getEmployee(employee_id)

    @overload
    def __init__(self, employee: IEmployee):
        self.employee = employee
        self.record = Solomon.getEmployee(employee.employee_id)

    @overload
    def __init__(self, employee: IEmployee, record: dict):
        self.employee = employee
        self.record = record

    @property
    @coerce
    def defaultSubAccount(self) -> ISubAccount:
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


registerAdapter(SolomonEmployee, IEmployee, ISolomonEmployee)
registerAdapter(SolomonEmployee, int, ISolomonEmployee)
