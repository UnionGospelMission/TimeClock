import TimeClock
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util.EmployeeProxy import EmployeeProxy
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.item import Item


@implementer(ICommand, IItem)
class AssumeRole(Item):
    name = text()
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return False
    @overload
    def hasPermission(self, caller: IPerson, employee: IEmployee=None) -> bool:
        if TimeClock.API.Permissions.AssumeRole not in caller.getPermissions():
            return False
        if IAdministrator(caller, None):
            return True
        sup = ISupervisor(caller, None)
        if not sup:
            return False
        return employee in sup.getEmployees()
    @overload
    def execute(self, caller: IPerson, employee: IEmployee):
        if self.hasPermission(caller, employee):
            c = CommandEvent(caller, self, employee)
            if IEventBus("Commands").postEvent(c):
                return EmployeeProxy(caller, employee)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        return self.execute(caller, ISubAccount(parameters[0]))
