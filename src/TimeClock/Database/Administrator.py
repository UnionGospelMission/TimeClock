from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Utils import overload, coerce
from axiom.attributes import reference
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.Util import Null
from axiom.item import Item


@implementer(IAdministrator)
class Administrator(Item):
    employee = reference()
    @coerce
    def getEmployees(self) -> [IEmployee]:
        return self.powerupsFor(ISupervisee)

    def approveTime(self, employee: IEmployee, time: ICalendarData):
        pass

    @overload
    def editTime(self, employee: IEmployee, time: ICalendarData, affected: ITimePeriod):
        pass

    @overload
    def editTime(self, employee: IEmployee, time: ITimePeriod, affected: ITimePeriod):
        pass

    @coerce
    def getPermissions(self) -> [IPermission]:
        return self.powerupsFor(IPermission)

    def addEmployee(self, employee: ISupervisee):
        self.powerUp(employee, ISupervisee)
        employee.supervisor = self

    # def setHoliday(self):


def makeAdministrator(*n):
    return Administrator(store=Store.Store)


registerAdapter(makeAdministrator, Null, IAdministrator)
registerAdapter(lambda n: n.employee, IAdministrator, IEmployee)
registerAdapter(lambda n: IAdministrator(n.employee), IAdministrator, ISupervisor)
