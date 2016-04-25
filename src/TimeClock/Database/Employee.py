from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IAssignedTask import IAssignedTask
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util.InMemoryTimePeriod import InMemoryTimePeriod
from ..ITimeClock.IDateTime import IDateTime

from TimeClock import API
from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import NULL
from axiom.attributes import text, integer, reference, boolean
from axiom.item import Item
from ..Exceptions import InvalidTransformation
from ..ITimeClock.IDatabase.ISubAccount import ISubAccount, IAbstractSubAccount
from ..ITimeClock.IDatabase.ICalendarData import ICalendarData
from ..ITimeClock.IDatabase.IEmployee import IEmployee
from ..ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from ..Utils import coerce, overload

SLRY = 1
HRLY = 2
TASK = 4


@implementer(IEmployee, ISupervisee)
class Employee(Item):
    emergency_contact_name = text()
    emergency_contact_phone = text()
    active_directory_name = text()
    employee_id = integer()
    alternate_authentication = reference()
    supervisor = reference()
    timeEntry = reference()
    hourly_by_task = boolean(default=False)

    @coerce
    def getTasks(self) -> [IAssignedTask]:
        return self.powerupsFor(IAssignedTask)

    def getCompensationType(self) -> tuple:
        ise = ISolomonEmployee(self.employee_id)
        if not ise:
            return None, None
        if ise.stdSlry:
            return ise.stdSlry, SLRY
        if self.hourly_by_task:
            return ise.stdUnitRate, TASK
        return ise.stdUnitRate, HRLY


    @coerce
    def getWorkLocations(self) -> [IWorkLocation]:
        return self.powerupsFor(IWorkLocation)

    @coerce
    def getSubAccounts(self) -> [IAbstractSubAccount]:
        return self.powerupsFor(ISubAccount)

    @coerce
    def getPermissions(self) -> [IPermission]:
        l = list(self.powerupsFor(IPermission))
        s = ISupervisor(self, None)
        if s:
            l.extend(s.getPermissions())
        return l

    def getAPI(self) -> IAPI:
        a = IAdministrator(self, None)
        if a:
            return API.APIs.AdministratorAPI.apiFor(self)
        s = ISupervisor(self, None)
        if s:
            return API.APIs.SupervisorAPI.apiFor(self)
        return API.APIs.EmployeeAPI.apiFor(self)

    def clockIn(self, subAccount: IAbstractSubAccount, workLocation: IWorkLocation) -> ITimeEntry:
        subAccount = ISubAccount(subAccount)
        if self not in subAccount.getEmployees():
            raise InvalidTransformation('User not authorized to work in area')
        if self.timeEntry:
            raise InvalidTransformation('User already clocked in')
        timeEntry = ITimeEntry(NULL)
        timeEntry.subAccount = subAccount
        timeEntry.type = IEntryType("Work")
        timeEntry.period = ITimePeriod(NULL)
        timeEntry.workLocation = workLocation
        self.powerUp(timeEntry, ITimeEntry)
        self.timeEntry = timeEntry
        return timeEntry

    def clockOut(self) -> ITimeEntry:
        timeEntry = list(self.powerupsFor(ITimeEntry))
        if (not timeEntry) or timeEntry[-1].period._endTime!=None:
            raise InvalidTransformation("User not currently clocked in")
        timeEntry = timeEntry[-1]
        timeEntry.period.end()
        self.timeEntry = None
        return timeEntry

    @coerce
    def isAdministrator(self) -> bool:
        return IAdministrator(self, False)

    @coerce
    def isSupervisor(self) -> bool:
        return ISupervisor(self, False)

    @overload
    def getEntries(self, area: ISubAccount, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.period.startTime() > startTime and e.period.endTime() > endTime]

    @overload
    def getEntries(self, entryType: IEntryType) -> [ITimeEntry]:
        entries = self.powerupsFor(ITimeEntry)
        return [e for e in entries if e.type == entryType]

    @overload
    def getEntries(self, area: ISubAccount) -> [ITimeEntry]:
        entries = self.powerupsFor(ITimeEntry)
        return [e for e in entries if e.area == area]

    @overload
    def getEntries(self, area: ISubAccount, entryType: IEntryType) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.type == entryType]

    @overload
    def getEntries(self, area: ISubAccount, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, startTime, endTime) if e.type == entryType]

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, entryType: IEntryType,
                   startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, entryType, startTime, endTime) if e.approved == approved]

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, startTime, endTime) if e.approved == approved]

    @overload
    def getEntries(self, area: ISubAccount, approved: bool) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.approved == approved]

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, entryType: IEntryType) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, entryType) if e.approved == approved]

    @overload
    def viewHours(self, area: IAbstractSubAccount) -> ICalendarData:
        return ICalendarData(self.getEntries(area, entryType="Work"))

    @overload
    def viewHours(self, area: IAbstractSubAccount, start: IDateTime, end: IDateTime) -> ICalendarData:
        return ICalendarData(self.getEntries(area, entryType="Work")).between(start, end)

    @overload
    def viewHours(self, start: IDateTime, end: IDateTime) -> ICalendarData:
        cd = ICalendarData(self.getEntries(entryType="Work"))
        return cd.between(start, end)

    @coerce
    def viewAverageHours(self, startTime: IDateTime, endTime: IDateTime) -> ICalendarData:
        endTime = endTime.replace(days=1)
        avgStart = startTime.replace(days=-90)
        hours = self.viewHours(start=avgStart, end=endTime)
        if hours.startTime() > startTime:
            startTime = hours.startTime().replace(seconds=-1)
        outdata = ICalendarData([])
        for day in startTime.daysBetween(startTime, endTime):
            if isinstance(day, tuple):
                continue
            total = hours.sumBetween(day.replace(days=-90), day)
            print(151, total)
            outdata.addTime(InMemoryTimePeriod(day, day + total / 90))
        return outdata



