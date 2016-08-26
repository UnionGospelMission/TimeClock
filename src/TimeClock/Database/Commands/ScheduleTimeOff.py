from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.Util import NULL
from ...ITimeClock.IDateTime import IDateTime

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
class ScheduleTimeOff(Item):
    typeName = 'timeclock_database_commands_schedulevacation_schedulevacation'
    name = text(default="Schedule Time Off")
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return True

    @overload
    def hasPermission(self, caller: IPerson, employee: ISupervisee) -> bool:
        return caller is employee or IAdministrator(caller, None) or (ISupervisor(caller, None) and employee in ISupervisor(caller).powerupsFor(ISupervisee))
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, start: IDateTime=None, duration: float = None, typ: IEntryType=None, sub: ISubAccount=None, loc: IWorkLocation=None) -> ITimeEntry:
        if self.hasPermission(caller, employee):
            c = CommandEvent(caller, self, employee, start, duration, typ)
            if IEventBus("Commands").postEvent(c):
                entry = ITimeEntry(NULL)
                entry.type = IEntryType(typ)
                entry.employee = employee
                entry.start(start)
                entry.end(entry.startTime().replace(hours=duration))
                entry.subAccount = sub
                entry.workLocation = loc
                employee.powerUp(entry, ITimeEntry)
                return entry
        else:
            print(caller)
            print(employee)
            raise PermissionDenied()
    @overload
    def execute(self, caller: IPerson, start: IDateTime, duration: float, typ: IEntryType) -> ITimeEntry:
        return self.execute(caller, caller, start, duration, typ)

    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        print(59, caller)
        print(60, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
