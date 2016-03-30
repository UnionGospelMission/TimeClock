from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from .ICalendarData import ICalendarData
from ..IReport import IReport
from .IEmployee import IEmployee


class IAdministrator(IPerson):
    employee = Attribute("employee")
    # def GenerateReport() -> IReport: pass
    # def getEmployee(name: str) -> IEmployee: pass
    # def getEmployee(EmployeeID: int) -> IEmployee: pass
    # def getEmployees() -> [IEmployee]: pass
    # def EditTime(employee: IEmployee, time: ICalendarData): pass
    # def ApproveTime(employee: IEmployee, time: ICalendarData): pass
    # def SetHoliday(time: ICalendarData, area: ISubAccount): pass

