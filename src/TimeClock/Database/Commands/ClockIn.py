from zope.interface import implementer

import TimeClock
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from axiom.item import Item


@implementer(ICommand, IItem)
class ClockIn(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return TimeClock.API.Permissions.ClockIn in permissions
    @overload
    def execute(self, caller: IPerson, subAccount: ISubAccount, workLocation: IWorkLocation):
        if self.hasPermission(IEmployee(caller).getPermissions()):
            c = CommandEvent(caller, self, subAccount, workLocation)
            if IEventBus("Commands").postEvent(c):
                IEmployee(caller).clockIn(subAccount, workLocation)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, employee: IEmployee, subAccount: ISubAccount, workLocation: IWorkLocation):
        if self.hasPermission(caller.getPermissions()):
            c = CommandEvent(caller, self, employee, subAccount, workLocation)
            if IEventBus("Commands").postEvent(c):
                employee.clockIn(subAccount, workLocation)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        return self.execute(caller, ISubAccount(int(parameters[0])), IWorkLocation(parameters[1]))
