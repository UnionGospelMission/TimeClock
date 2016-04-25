from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IAssignedTask import IAssignedTask
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IDateTime import IDateTime


from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Utils import overload, fromFunction
from .ISubAccount import IAbstractSubAccount as ISubAccount
from .ICalendarData import ICalendarData
from .ITimeEntry import ITimeEntry


class IEmployee(IPerson):
    emergency_contact_name = Attribute("emergency_contact_name", 'str')
    emergency_contact_phone = Attribute("emergency_contact_phone", 'str')
    active_directory_name = Attribute("active_directory_name", 'str')
    employee_id = Attribute("employee_id", 'int')
    alternate_authentication = Attribute("alternate_authentication", 'reference')
    supervisor = Attribute("supervisor", 'reference')

    hourly_by_task = Attribute("hourly_by_task", 'bool')

    def getCompensationType() -> tuple:
        pass

    def getTasks() -> [IAssignedTask]:
        pass

    def clockIn(area: ISubAccount, workLocation: IWorkLocation) -> ITimeEntry:
        pass

    def clockOut() -> ITimeEntry:
        pass

    def viewHours(area: ISubAccount) -> ICalendarData:
        pass

    def viewAverageHours(startTime: IDateTime, endTime: IDateTime) -> ICalendarData:
        pass

    def isSupervisor() -> bool:
        pass

    def isAdministrator() -> bool:
        pass

    @overload
    def getEntries(area: ISubAccount, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount, entryType: IEntryType) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount, approved: bool, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount, approved: bool, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        pass

    @overload
    def getEntries(area: ISubAccount, approved: bool) -> [ITimeEntry]:
        pass

    @fromFunction
    @overload
    def getEntries(area: ISubAccount, approved: bool, entryType: IEntryType) -> [ITimeEntry]:
        pass

    def getSubAccounts() -> [ISubAccount]:
        pass

    def getWorkLocations() -> [IWorkLocation]:
        pass

    def getAPI() -> IAPI:
        pass



