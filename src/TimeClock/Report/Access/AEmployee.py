from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Report.IAccess.IACalendarData import IACalendarData
from TimeClock.Report.IAccess.IASubAccount import IASubAccount
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation
from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import coerce, overload
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Report.IAccess.IAEmployee import IAEmployee


@adapter(IEmployee, IAEmployee)
@implementer(IAEmployee)
class AEmployee(object):
    __slots__ = ['_employee']

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._employee is other._employee

    @coerce
    def __init__(self, emp: IEmployee):
        self._employee = emp

    @property
    def employee_id(self):
        return self._employee.employee_id

    @property
    def name(self):
        return self._employee.name

    @property
    def active_directory_name(self):
        return self._employee.active_directory_name

    @property
    @coerce
    def defaultSubAccount(self) -> IASubAccount:
        return ISolomonEmployee(self._employee).defaultSubAccount

    @property
    def phone(self):
        return ISolomonEmployee(self._employee).phone

    @property
    @coerce
    def defaultWorkLocation(self) -> IAWorkLocation:
        return ISolomonEmployee(self._employee).defaultWorkLocation

    @property
    def payGrpId(self):
        return ISolomonEmployee(self._employee).payGrpId

    @property
    def stdSlry(self):
        return ISolomonEmployee(self._employee).stdSlry

    @property
    def status(self):
        return ISolomonEmployee(self._employee).status

    @property
    def hourly_by_task(self):
        return self._employee.hourly_by_task

    @overload
    def getSupervisors(self) -> [IAEmployee]:
        return [IAEmployee(i.employee) for i in self._employee.getSupervisors()]

    @overload
    def getSupervisors(self, area) -> [IAEmployee]:
        a = ISubAccount(area)
        return [IAEmployee(i.employee) for i in self._employee.getSupervisors() if a in i.getSubAccounts()]

    @property
    def emergency_contact_name(self):
        return self._employee.emergency_contact_name

    @property
    def emergency_contact_phone(self):
        return self._employee.emergency_contact_phone

    def getCompensationType(self) -> [float]:
        return self._employee.getCompensationType()

    @coerce
    def getSubAccounts(self) -> [IASubAccount]:
        return self._employee.getSubAccounts()

    @coerce
    def getWorkLocations(self) -> [IAWorkLocation]:
        return self._employee.getWorkLocations()

    @coerce
    def getTimeEntries(self, startTime: IDateTime, endTime: IDateTime) -> IACalendarData:
        return self._employee.getEntries(startTime=startTime, endTime=endTime)

    @coerce
    def getApprovedTimeEntries(self, startTime, endTime) -> IACalendarData:
        return self._employee.getApprovedEntries(startTime, endTime)

    @overload
    def viewHours(self, startTime: IDateTime, endTime: IDateTime) -> IACalendarData:
        return self._employee.viewHours(startTime, endTime)

    @overload
    def viewHours(self, startTime: IDateTime, endTime: IDateTime, approved: bool) -> IACalendarData:
        return self._employee.viewHours(startTime, endTime, approved)

