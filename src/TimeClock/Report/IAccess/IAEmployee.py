from zope.interface import Attribute

from TimeClock.Report.IAccess import IACalendarData
from TimeClock.Report.IAccess.IASubAccount import IASubAccount
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible

SLRY = 1
HRLY = 2


class IAEmployee(IAbstractAccessible):
    employee_id = Attribute('employee_id')
    name = Attribute('name')
    active_directory_name = Attribute('active_directory_name')
    defaultSubAccount = Attribute("defaultArea")
    phone = Attribute("Phone")
    defaultWorkLocation = Attribute("defaultWorkLocation")
    stdSlry = Attribute("Standard Salary")
    payGrpId = Attribute("Pay group Id (PT/REGHR)")
    status = Attribute("Status")
    hourly_by_task = Attribute('hourly_by_task')
    emergency_contact_name = Attribute('emergency_contact_name')
    emergency_contact_phone = Attribute('emergency_contact_phone')


    def getCompensationType() -> [float]:
        """
        Returns [compensation rate, {SLRY} or {HRLY}]
        """

    def getSubAccounts() -> [IASubAccount]:
        """
        Returns a list of sub accounts associated with the employee
        """

    def getWorkLocations() -> [IAWorkLocation]:
        """
        Returns a list of work locations associated with the employee
        """

    def getTimeEntries(startTime, endTime) -> IACalendarData:
        """
        Returns all time entries associated with the employee between startTime and endTime
        """

    def viewHours(startTime, endTime) -> IACalendarData:
        """
        Returns all IEntryType("Work") time entries between startTime and endTime
        """

    def getSupervisors():
        """
        Returns list of this employees supervisors
        """
