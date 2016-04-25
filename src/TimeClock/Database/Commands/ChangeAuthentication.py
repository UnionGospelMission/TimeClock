from zope.interface import Attribute, implementer, Interface

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Database.StaticAuthenticationMethod import StaticAuthenticationMethod
from TimeClock.Exceptions import InvalidTransformation, PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util import NULL
from TimeClock.Utils import overload
from axiom.item import Item
from axiom.attributes import text
from TimeClock.Solomon.Solomon import getEmployees


@implementer(ICommand, IItem)
class ChangeAuthentication(Item):
    name = text()
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return (not caller.active_directory_name) and self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]):
        return True
    @overload
    def execute(self, caller: IPerson, oldpw: str, newpw: str, newpwa: str):
        caller = IEmployee(caller)
        c = CommandEvent(caller, self)
        IEventBus("Commands").postEvent(c)
        if caller.active_directory_name:
            raise InvalidTransformation("Cannot change active directory password here")
        if newpw != newpwa:
            raise ValueError("Password and password confirmation do not match")

        if caller.alternate_authentication:
            if not caller.alternate_authentication.authenticate(caller, oldpw):
                raise PermissionDenied("Incorrect old password")
            caller.alternate_authentication.setPassword(newpw)
        else:
            caller.alternate_authentication = StaticAuthenticationMethod(store=self.store).setPassword(newpw)
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(42, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
