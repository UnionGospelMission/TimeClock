from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Report.IAccess.IACalendarData import IACalendarData
from TimeClock.Report.IAccess.IASubAccount import IASubAccount
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation
from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import coerce
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Report.IAccess.IAEmployee import IAEmployee


@adapter(IEmployee, IAEmployee)
@implementer(IAEmployee)
class AEmployee(object):
    __slots__ = ['_employee']

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
    def stdSlry(self):
        return ISolomonEmployee(self._employee).stdSlry

    @property
    def status(self):
        return ISolomonEmployee(self._employee).status

    @property
    def hourly_by_task(self):
        return self._employee.hourly_by_task

    @property
    def supervisor(self) -> IAEmployee:
        if self._employee.supervisor:
            return IAEmployee(self._employee.supervisor.employee)

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
    def viewHours(self, startTime, endTime) -> IACalendarData:
        return self._employee.viewHours(startTime, endTime)

