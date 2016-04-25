from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from ...ITimeClock.IDateTime import IDateTime

from TimeClock import AD
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class EditTime(Item):
    name = text()
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, caller: ISupervisor, employee: ISupervisee, entry: ITimeEntry) -> bool:
        return IAdministrator(caller, None) or (not entry.approved and employee in caller.powerupsFor(ISupervisee))
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return False
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, entry: ITimeEntry, start: IDateTime=None, end: IDateTime=None):
        if self.hasPermission(caller, employee, entry):
            c = CommandEvent(caller, self, employee, entry, start, end)
            if IEventBus("Commands").postEvent(c):
                if start:
                    entry.period.start(start)
                if end:
                    entry.period.end(end)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
