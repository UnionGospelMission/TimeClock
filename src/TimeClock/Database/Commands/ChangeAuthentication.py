from zope.interface import Attribute, implementer, Interface

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Database.LDAPBackedAuthenticationMethod import LDAPBackedAuthenticationMethod
from TimeClock.Database.StaticAuthenticationMethod import StaticAuthenticationMethod
from TimeClock.Exceptions import InvalidTransformation, PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class ChangeAuthentication(Item):
    name = text()

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return ((not caller.active_directory_name) or caller.alternate_authentication and caller.alternate_authentication.expired) and self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]):
        return True

    @overload
    def execute(self, caller: IAdministrator, employee: IEmployee, newpw: str, newpwa: str):
        c = CommandEvent(caller, self, employee)
        IEventBus("Commands").postEvent(c)
        if employee.active_directory_name:
            raise InvalidTransformation("Cannot change active directory password here")
        if newpw != newpwa:
            raise ValueError("Password and password confirmation do not match")
        if employee.alternate_authentication:
            employee.alternate_authentication.setPassword(newpw)
        else:
            employee.alternate_authentication = StaticAuthenticationMethod(store=self.store).setPassword(newpw)
        employee.alternate_authentication.expired = True
        return True

    @overload
    def execute(self, caller: IPerson, oldpw: str, newpw: str, newpwa: str):
        caller = IEmployee(caller)
        c = CommandEvent(caller, self)
        IEventBus("Commands").postEvent(c)
        if newpw != newpwa:
            raise ValueError("Password and password confirmation do not match")

        if caller.active_directory_name:
            if isinstance(caller.alternate_authentication, LDAPBackedAuthenticationMethod):
                return caller.alternate_authentication.setPassword(caller, newpw)
            else:
                raise InvalidTransformation("Cannot change active directory password here")

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
