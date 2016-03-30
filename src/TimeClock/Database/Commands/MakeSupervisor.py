from zope.interface import implementer

import TimeClock
from TimeClock.Database import Permissions
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from axiom.item import Item


@implementer(ICommand, IItem)
class MakeSupervisor(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return TimeClock.API.Permissions.MakeSupervisor in permissions
    @overload
    def execute(self, caller: IPerson, employee: IEmployee):
        if self.hasPermission(caller.getPermissions()):
            c = CommandEvent(caller, self, employee)
            if IEventBus("Commands").postEvent(c):
                s = ISupervisor(employee, None)
                if s is None:
                    s = ISupervisor(NULL)
                    employee.powerUp(s, ISupervisor)
                    s.employee = employee
            else:
                raise PermissionDenied()
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        print(32, self, caller, parameters, sep='\n')
        raise NotImplementedError("%s called with invalid parameters"%self.name)
