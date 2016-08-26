from zope.interface import implementer

from TimeClock.Database.Commands.CommandEvent import CommandEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Utils import overload
from axiom.item import Item

from axiom.attributes import text


@implementer(ICommand, IItem)
class SetSubAccounts(Item):
    name = text()

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IAdministrator, employee: IEmployee, locations: list):
        c = CommandEvent(caller, self, employee, locations)
        IEventBus("Commands").postEvent(c)
        current = employee.getSubAccounts()
        for c in current:
            if c not in locations:
                employee.powerDown(c, ISubAccount)
                c.powerDown(employee, IEmployee)
        for a in locations:
            a = ISubAccount(a)
            if a not in current:
                employee.powerUp(a, ISubAccount)
                a.powerUp(employee, IEmployee)
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
