from zope.interface import implementer

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
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
class ClockOut(Item):
    def getArguments(self) -> [object]:
        return ["caller", {"Employee ID":"optional"}]
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson):
        if self.hasPermission(caller.getPermissions()):
            c = CommandEvent(caller, self)
            if IEventBus("Commands").postEvent(c):
                IEmployee(caller).clockOut()
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, employee: IEmployee):
        if self.hasPermission(caller.getPermissions()):
            c = CommandEvent(caller, self, employee)
            if IEventBus("Commands").postEvent(c):
                employee.clockOut()
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters"%self.name)
