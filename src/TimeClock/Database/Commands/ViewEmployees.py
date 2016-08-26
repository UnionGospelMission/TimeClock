from zope.interface import implementer

from TimeClock.Database.Employee import Employee
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from axiom.item import Item

from axiom.attributes import text
from TimeClock.ITimeClock.IDateTime import IDateTime

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload, coerce


@implementer(ICommand, IItem)
class ViewEmployees(Item):
    name = text()

    @overload
    def hasPermission(self, caller: IAdministrator) -> bool:
        return True

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return IAdministrator(caller, None) or ISupervisor(caller, None)
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson):
        if self.hasPermission(caller):
            c = CommandEvent(caller, self)
            if IEventBus("Commands").postEvent(c):
                return list(ISupervisor(caller).powerupsFor(ISupervisee))
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IAdministrator, area: ISubAccount) -> object:
        if self.hasPermission(caller):
            c = CommandEvent(caller, self, area)
            if IEventBus("Commands").postEvent(c):
                if area:
                    return list(area.getEmployees())
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IAdministrator, area: str) -> object:
        if ISubAccount(area, None):
            return self.execute(caller, ISubAccount(area))
        return list(self.store.query(Employee))
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
