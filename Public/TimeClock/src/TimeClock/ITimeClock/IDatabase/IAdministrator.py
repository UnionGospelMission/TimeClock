from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from .ICalendarData import ICalendarData
from ..IReport import IReport
from .IEmployee import IEmployee


class IAdministrator(IItem):
    employee = Attribute("employee")
    # def GenerateReport() -> IReport: pass
    def getEmployee(name: str) -> IEmployee: pass
    def getEmployee(EmployeeID: int) -> IEmployee: pass
    def getEmployees() -> [IEmployee]: pass
    # def EditTime(employee: IEmployee, time: ICalendarData): pass
    # def ApproveTime(employee: IEmployee, time: ICalendarData): pass
    def SetHoliday(time: ICalendarData, area: IArea): pass
