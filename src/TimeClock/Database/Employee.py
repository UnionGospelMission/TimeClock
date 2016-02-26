from zope.interface import implementer
from zope.interface.common.idatetime import IDateTime

from TimeClock.API import AdministratorAPI, EmployeeAPI
from TimeClock.API import SupervisorAPI
from TimeClock.ITimeClock.IAPI import IAPI
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import NULL
from axiom.attributes import text, integer, reference
from axiom.item import Item

from ..ITimeClock.IDatabase.IArea import IArea, IAbstractArea
from ..ITimeClock.IDatabase.ICalendarData import ICalendarData
from ..ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from ..ITimeClock.IDatabase.IEmployee import IEmployee
from ..Exceptions import InvalidTransformation
from ..Utils import coerce, overload


@implementer(IEmployee, ISupervisee)
class Employee(Item):
    emergency_contact_name = text()
    emergency_contact_phone = text()
    active_directory_name = text()
    employee_id = integer()
    alternate_authentication = reference()
    supervisor = reference()
    timeEntry = reference()

    @coerce
    def getAreas(self) -> [IAbstractArea]:
        return self.powerupsFor(IArea)

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
            return AdministratorAPI
        s = ISupervisor(self, None)
        if s:
            return SupervisorAPI
        return EmployeeAPI

    def clockIn(self, area: IAbstractArea) -> ITimeEntry:
        area = IArea(area)
        if self not in area.getEmployees():
            raise InvalidTransformation('User not authorized to work in area')
        if self.timeEntry:
            raise InvalidTransformation('User already clocked in')
        timeEntry = ITimeEntry(NULL)
        timeEntry.area = area
        timeEntry.type = IEntryType("Work")
        timeEntry.period = ITimePeriod(NULL)
        self.powerUp(timeEntry, ITimeEntry)
        self.timeEntry = timeEntry
        return timeEntry

    def clockOut(self) -> ITimeEntry:
        timeEntry = list(self.powerupsFor(ITimeEntry))
        if not timeEntry:
            raise InvalidTransformation("User not currently clocked in")
        timeEntry = timeEntry[0]
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
    def getEntries(self, area: IArea, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.period.startTime() > startTime and e.period.endTime() > endTime]

    @overload
    def getEntries(self, area: IArea) -> [ITimeEntry]:
        entries = self.powerupsFor(ITimeEntry)
        return [e for e in entries if e.area == area]

    @overload
    def getEntries(self, area: IArea, entryType: IEntryType) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.type == entryType]

    @overload
    def getEntries(self, area: IArea, entryType: IEntryType, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, startTime, endTime) if e.type == entryType]

    @overload
    def getEntries(self, area: IArea, approved: bool, entryType: IEntryType,
                   startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, entryType, startTime, endTime) if e.approved == approved]

    @overload
    def getEntries(self, area: IArea, approved: bool, startTime: IDateTime, endTime: IDateTime) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, startTime, endTime) if e.approved == approved]

    @overload
    def getEntries(self, area: IArea, approved: bool) -> [ITimeEntry]:
        return [e for e in self.getEntries(area) if e.approved == approved]

    @overload
    def getEntries(self, area: IArea, approved: bool, entryType: IEntryType) -> [ITimeEntry]:
        return [e for e in self.getEntries(area, entryType) if e.approved == approved]

    def viewHours(self, area: IAbstractArea) -> ICalendarData:
        return ICalendarData(self.getEntries(area, entryType="Work"))

    def viewAverageHours(self, area: IAbstractArea) -> ICalendarData:
        # TODO: Fix average hours
        raise NotImplementedError()


