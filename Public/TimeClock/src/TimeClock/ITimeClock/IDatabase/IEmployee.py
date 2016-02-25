from twisted.python.components import registerAdapter
from zope.interface import Interface, Attribute
from zope.interface.common.idatetime import IDateTime

from TimeClock.Axiom.Store import Store

from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Util import Null
from TimeClock.Utils import overload, fromFunction
from .IArea import IAbstractArea as IArea
from .ICalendarData import ICalendarData
from .ITimeEntry import ITimeEntry


class IEmployee(IItem):
    emergency_contact_name = Attribute("emergency_contact_name")
    emergency_contact_phone = Attribute("emergency_contact_phone")
    active_directory_name = Attribute("active_directory_name")
    employee_id = Attribute("employee_id")
    alternate_authentication = Attribute("alternate_authentication")
    supervisor = Attribute("supervisor")

    def clockIn(area: IArea) -> ITimeEntry:
        pass

    def clockOut() -> ITimeEntry:
        pass

    def viewHours(area: IArea) -> ICalendarData:
        pass

    def viewAverageHours(area: IArea) -> ICalendarData:
        pass

    def isSupervisor() -> bool:
        pass

    def isAdministrator() -> bool:
        pass

    @overload
    def getEntries(area: IArea, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea, entryType: IEntryType) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea, approved: bool, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea, approved: bool, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: IArea, approved: bool) -> [ITimeEntry]:
        pass

    @fromFunction
    @overload
    def getEntries(area: IArea, approved: bool, entryType: IEntryType) -> [ITimeEntry]:
        pass

    def getAreas() -> [IArea]:
        pass

    def getPermissions() -> [IPermission]:
        pass

    def getAPI() -> IAPI:
        pass




def newEmployee(x):
    from TimeClock.Database import Employee
    from TimeClock.Database.Permissions import ClockIn
    e = Employee(store=Store)
    e.powerUp(ClockIn, IPermission)
    return e


registerAdapter(newEmployee, Null, IEmployee)
