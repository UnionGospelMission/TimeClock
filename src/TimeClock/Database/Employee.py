from zope.interface import implementer

from TimeClock import Utils
from TimeClock.Axiom import Transaction
from TimeClock.Database.Event.ClockInOutEvent import ClockInOutEvent
from TimeClock.ITimeClock.IDatabase.IAssignedTask import IAssignedTask
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisedBy import ISupervisedBy
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util.InMemoryTimePeriod import InMemoryTimePeriod
from axiom.upgrade import registerAttributeCopyingUpgrader, registerUpgrader
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
from axiom.attributes import text, integer, reference, boolean, AND, OR
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
    schemaVersion = 2
    emergency_contact_name = text()
    emergency_contact_phone = text()
    active_directory_name = text()
    employee_id = integer()
    alternate_authentication = reference()

    timeEntry = reference()
    hourly_by_task = boolean(default=False)

    @property
    def name(self):
        return ISolomonEmployee(self).name

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

    @Transaction
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
        timeEntry.employee = self
        self.powerUp(timeEntry, ITimeEntry)
        self.timeEntry = timeEntry
        e = ClockInOutEvent(self)
        IEventBus("Database").postEvent(e)
        return timeEntry

    @Transaction
    def clockOut(self) -> ITimeEntry:
        timeEntry = self.timeEntry
        if (not timeEntry) or timeEntry.period._endTime != None:
            raise InvalidTransformation("User not currently clocked in")
        timeEntry.period.end()
        self.timeEntry = None
        e = ClockInOutEvent(self)
        IEventBus("Database").postEvent(e)
        return timeEntry

    @coerce
    def isAdministrator(self) -> bool:
        return IAdministrator(self, False)

    @coerce
    def isSupervisor(self) -> bool:
        return ISupervisor(self, False)

    @overload
    def getEntries(self):
        return list(self.powerupsFor(ITimeEntry))

    @overload
    def getEntries(self, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        from TimeClock.Database.TimePeriod import TimePeriod
        from TimeClock.Database.TimeEntry import TimeEntry
        return [e for e in self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod),
                                            comparison=AND(
                                                TimeEntry.period==TimePeriod.storeID,
                                                TimeEntry.employee==self,
                                                TimePeriod._startTime<=endTime,
                                                OR(
                                                    TimePeriod._endTime >= startTime,
                                                    TimePeriod._endTime == None
                                                )

                                            )) if
                e.period.startTime() < endTime and e.period.endTime() > startTime]

    @overload
    def getEntries(self, area: ISubAccount, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(startTime, endTime) if e.subAccount == area]

    @overload
    def getEntries(self, entryType: IEntryType) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry,), comparison=AND(
            TimeEntry.employee==self,
            TimeEntry.type==entryType
        ))
        return list(entries)

    @overload
    def getEntries(self, area: ISubAccount) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry,), comparison=AND(
            TimeEntry.employee==self,
            TimeEntry.subAccount==area,
            TimeEntry.denied==False
        ))
        return list(entries)

    @overload
    def getEntries(self, area: ISubAccount, entryType: IEntryType) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry,), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.denied==False,
            TimeEntry.type==entryType
        ))
        return entries

    @overload
    def getEntries(self, area: ISubAccount, loc: IWorkLocation, approved: bool, entryType: IEntryType,
                   startTime: IDateTime,
                   endTime: IDateTime) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.workLocation == loc,
            TimeEntry.approved == approved,
            TimeEntry.type == entryType,
            TimeEntry.period==TimePeriod.storeID,
            TimePeriod._startTime >= endTime,
            OR(
                TimePeriod._endTime >= startTime,
                TimePeriod._endTime == None
            )
        ))

        return entries

    @overload
    def getEntries(self, area: ISubAccount, loc: IWorkLocation, entryType: IEntryType, startTime: IDateTime,
                   endTime: IDateTime) -> [
        ITimeEntry]:

        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.workLocation == loc,
            TimeEntry.type == entryType,
            TimeEntry.period == TimePeriod.storeID,
            TimePeriod._startTime >= endTime,
            OR(
                TimePeriod._endTime >= startTime,
                TimePeriod._endTime == None
            )
        ))

        return entries

    @overload
    def getEntries(self, area: ISubAccount, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [
        ITimeEntry]:

        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.type == entryType,
            TimeEntry.period == TimePeriod.storeID,
            TimePeriod._startTime >= endTime,
            OR(
                TimePeriod._endTime >= startTime,
                TimePeriod._endTime == None
            )
        ))
        return entries

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, entryType: IEntryType,
                   startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:

        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.approved == approved,
            TimeEntry.type == entryType,
            TimeEntry.period == TimePeriod.storeID,
            TimePeriod._startTime >= endTime,
            OR(
                TimePeriod._endTime >= startTime,
                TimePeriod._endTime == None
            )
        ))
        return entries

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry, TimePeriod), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.approved == approved,
            TimeEntry.period == TimePeriod.storeID,
            TimePeriod._startTime >= endTime,
            OR(
                TimePeriod._endTime >= startTime,
                TimePeriod._endTime == None
            )
        ))

        return entries

    @overload
    def getEntries(self, area: ISubAccount, approved: bool) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.approved == approved,
        ))
        return entries

    @overload
    def getEntries(self, area: ISubAccount, approved: bool, entryType: IEntryType) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry), comparison=AND(
            TimeEntry.employee == self,
            TimeEntry.subAccount == area,
            TimeEntry.approved == approved,
            TimeEntry.type == entryType,
        ))
        return entries

    @coerce
    def getApprovedEntries(self, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        from TimeClock.Database.TimeEntry import TimeEntry
        from TimeClock.Database.TimePeriod import TimePeriod
        return self.powerupsFor(ITimeEntry,
                                tables=(TimeEntry, TimePeriod),
                                comparison=AND(
                                    TimeEntry.approved==True,
                                    TimeEntry.employee==self,
                                    TimeEntry.period==TimePeriod.storeID,
                                    TimePeriod._startTime<=endTime,
                                    OR(
                                        TimePeriod._endTime >= startTime,
                                        TimePeriod._endTime == None
                                    )
                                ))

    @overload
    def viewHours(self, area: IAbstractSubAccount) -> ICalendarData:
        return ICalendarData(self.getEntries(area, entryType="Work"))

    @overload
    def viewHours(self, area: IAbstractSubAccount, start: IDateTime, end: IDateTime) -> ICalendarData:
        return ICalendarData(self.getEntries(area, entryType="Work")).between(start, end)

    @overload
    def viewHours(self, start: IDateTime, end: IDateTime) -> ICalendarData:
        work = IEntryType("Work")
        cd = ICalendarData([i for i in self.getEntries(start, end) if i.type==work])
        return cd.between(start, end)

    @overload
    def viewHours(self, start: IDateTime, end: IDateTime, approved: bool) -> ICalendarData:
        work = IEntryType("Work")
        cd = ICalendarData([i for i in self.getEntries(start, end) if i.approved == approved and i.type==work])
        return cd.between(start, end)

    @overload
    def viewHours(self, area: ISubAccount, loc: IWorkLocation, approved: bool, entryType: IEntryType, start: IDateTime,
                  end: IDateTime) -> ICalendarData:
        from TimeClock.Database.TimeEntry import TimeEntry
        entries = self.powerupsFor(ITimeEntry, tables=(TimeEntry,), comparison=AND(
            TimeEntry.approved == approved,
            TimeEntry.employee == self,
            TimeEntry.workLocation == loc,
            TimeEntry.subAccount == area
        ))
        return ICalendarData(list(entries)).between(start, end)

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

    def getSupervisors(self):
        return self.powerupsFor(ISupervisedBy)


def upgrade_1_2(old: Employee):
    supervisor = old.supervisor
    keys = dict((str(name), getattr(old, name))
                for (name, _) in old.getSchema())
    keys.pop('supervisor')
    newitem = old.upgradeVersion(Employee.typeName, 1, 2, **keys)
    if supervisor:
        newitem.powerUp(supervisor, ISupervisedBy)

registerUpgrader(upgrade_1_2, Employee.typeName, 1, 2)
