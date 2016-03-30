from zope.interface import implementer

from TimeClock import AD
from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class ApproveTime(Item):
    name = text()
    @overload
    def hasPermission(self, caller: IPerson, employee: ISupervisee) -> bool:
        return IAdministrator(caller, None) or employee in ISupervisor(caller).powerupsFor(ISupervisee)
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, entry: ITimeEntry):
        if self.hasPermission(caller, employee) and entry.endTime(False):
            c = CommandEvent(caller, self, employee, entry)
            if IEventBus("Commands").postEvent(c):
                print(35)
                entry.approved = True
            else:
                print(37)
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, entries: list):
        for e in entries:
            self.execute(caller, employee, e)
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
