from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.item import Item

from axiom.attributes import text
from TimeClock.ITimeClock.IDateTime import IDateTime

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload, coerce


@implementer(ICommand, IItem)
class ViewHours(Item):
    def getArguments(self) -> [object]:
        return ["caller", "Employee ID", "area", "start date", "end date"]
    name = text()
    @overload
    def hasPermission(self, caller: IEmployee, employee: ISupervisee) -> bool:
        return IAdministrator(caller, None) or (ISupervisor(caller, None) and employee in ISupervisor(caller).getEmployees()) or caller is employee
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IEmployee, employee: ISupervisee, start: IDateTime,
                end: IDateTime):
        print(37, caller, employee, start, end)
        if self.hasPermission(caller, employee):
            c = CommandEvent(caller, self, employee, start, end)
            if IEventBus("Commands").postEvent(c):
                return employee.viewHours(start=start, end=end)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, employee: ISupervisee, area: IArea, start: IDateTime=None, end: IDateTime=None):
        print(46)
        if self.hasPermission(caller, employee):
            c = CommandEvent(caller, self, employee, area, start=start, end=end)
            if IEventBus("Commands").postEvent(c):
                return employee.viewHours(area, start, end)
        else:
            raise PermissionDenied()

    @overload
    def execute(self, caller: IEmployee, start: IDateTime, end: IDateTime):
        print(56, start, end)
        return self.execute(caller, caller, start=start, end=end)
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
