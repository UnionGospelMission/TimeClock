from zope.interface import implementer

import twisted.internet.defer
from TimeClock import AD
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import coerce, overload
from axiom.item import Item
from axiom.attributes import text
from TimeClock.Database.LDAPBackedAuthenticationMethod import LDAPBackedAuthenticationMethod


@implementer(ICommand, IItem)
class AsyncLogin(Item):
    name = text(default="Async Login")
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return True

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True

    @coerce
    def asyncLogin(self, caller: object, employee: IEmployee, pw: str):
        if not employee.alternate_authentication:
            if employee.active_directory_name:
                employee.alternate_authentication = LDAPBackedAuthenticationMethod(store=employee.store)
            else:
                return twisted.internet.defer.succeed(False)
        allowed = employee.alternate_authentication.authenticate(employee, pw)
        if not allowed:
            return twisted.internet.defer.succeed(False)
        if not isinstance(allowed, twisted.internet.defer.Deferred):
            return twisted.internet.defer.succeed(allowed)

        def assertSucceed(v):
            if not v:
                raise PermissionDenied("Incorrect Username or Password")
            return v

        def postEvent(v):
            c = CommandEvent(caller, self, employee)
            c.retval = v
            if IEventBus("Commands").postEvent(c):
                return c.retval
            return False

        allowed.addCallback(assertSucceed)
        allowed.addCallback(postEvent)
        return allowed

    @overload
    def execute(self, caller: object, employee: IEmployee, pw: str):
        return self.asyncLogin(caller, employee, pw)

    @overload
    def execute(self, caller: object, eid: int, pw: str):
        return self.asyncLogin(caller, eid, pw)

    @overload
    def execute(self, caller: object, adid: str, pw: str):
        return self.asyncLogin(caller, adid, pw)

    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
