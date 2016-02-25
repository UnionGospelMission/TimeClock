from collections import defaultdict

from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.API import AdministratorAPI
from TimeClock.Database import Employee
from TimeClock.Database.Permissions import Permission
from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IArea import IArea, IAbstractArea
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.Utils import overload


@implementer(IEmployee, ISupervisor, IAdministrator, IItem)
class ConsoleAdministratorClass(object):
    emergency_contact_name = None
    emergency_contact_phone = None
    active_directory_name = None
    employee_id = None
    alternate_authentication = None
    supervisor = None

    def __init__(self):
        self.powerups = defaultdict(list)
        self.employee = self
    @overload
    def unimplemented(self) -> object:
        raise NotImplementedError("Console Administrator")
    @overload
    def unimplemented(self, other: object) -> object:
        self.unimplemented()
    @overload
    def unimplemented(self, other: object, other2: object, other3: object) -> object:
        self.unimplemented()
    @overload
    def unimplemented(self, other: object, other2: object, other3: object, other4: object) -> object:
        self.unimplemented()
    @overload
    def unimplemented(self, other: object, other2: object, other3: object, other4: object, other5: object) -> object:
        self.unimplemented()
    def clockIn(self, area: IAbstractArea) -> ITimeEntry:
        self.unimplemented()
    def viewHours(self, area: IAbstractArea) -> ICalendarData:
        self.unimplemented()
    def getAreas(self) -> [IAbstractArea]:
        self.unimplemented()
    getEntries = unimplemented
    viewAverageHours = viewHours
    def addEmployee(self, e: IEmployee):
        self.unimplemented()
    def clockOut(self) -> IAbstractArea:
        self.unimplemented()
    def isAdministrator(self) -> bool:
        return True
    def isSupervisor(self) -> bool:
        return True
    def powerUp(self, other, iface):
        self.powerups[iface].append(other)
    def getPermissions(self) -> [IPermission]:
        return Store.query(Permission)
    def getAPI(self) -> IAPI:
        return AdministratorAPI
    def getEmployees(self) -> IEmployee:
        return Store.query(Employee)
    @overload
    def getEmployee(self, name: str) -> IEmployee:
        return next(Store.query(Employee, Employee.active_directory_name == name))
    @overload
    def getEmployee(self, EmployeeID: int) -> IEmployee:
        return next(Store.query(Employee, Employee.employee_id == EmployeeID))
    def SetHoliday(self, time: ICalendarData, area: IArea):
        #TODO
        raise NotImplementedError("Holidays not done yet")


ConsoleAdministrator = ConsoleAdministratorClass()
