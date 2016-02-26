from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from . import Solomon


@implementer(ISolomonEmployee)
class SolomonEmployee(object):
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
    def defaultArea(self) -> IArea:
        area = IArea(self.dfltExpSub, None)
        if not area:
            area = IArea(NULL)
            s_area = Solomon.getArea(self.dfltExpSub)
            area.name = s_area['description']
            area.sub = self.dfltExpSub
        return area

    @property
    @coerce
    def defaultWorkLocation(self) -> IWorkLocation:
        wl = IWorkLocation(self.dfltWrkloc, None)
        if not wl:
            wl = IWorkLocation(NULL)
            wl.id = self.dfltWrkloc
            wl.description = Solomon.getWorkLocation(self.dfltWrkloc)['Descr']
        return wl

    def __getattr__(self, item):
        for i in self.record:
            if i[0].lower() + i[1:] == item:
                return self.record[i]

registerAdapter(SolomonEmployee, IEmployee, ISolomonEmployee)
