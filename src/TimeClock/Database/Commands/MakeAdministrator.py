from zope.interface import implementer

import TimeClock
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from axiom.item import Item


@implementer(ICommand, IItem)
class MakeAdministrator(Item):
    name = text()
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return TimeClock.API.Permissions.MakeSupervisor in permissions
    @overload
    def execute(self, caller: IPerson, employee: IEmployee):
        if self.hasPermission(caller.getPermissions()):
            c = CommandEvent(caller, self, employee)
            if IEventBus("Commands").postEvent(c):
                s = IAdministrator(employee, None)
                if s is None:
                    s = IAdministrator(NULL)
                    employee.powerUp(s, IAdministrator)
            else:
                raise PermissionDenied()
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
