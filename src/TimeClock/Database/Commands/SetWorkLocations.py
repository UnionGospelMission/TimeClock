from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.IWorkLocations import IWorkLocations
from TimeClock.Utils import overload
from axiom.item import Item

from axiom.attributes import text


@implementer(ICommand, IItem)
class SetWorkLocations(Item):
    name = text()
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IAdministrator, employee: IEmployee, areas: [IWorkLocations]):
        current = employee.getWorkLocations()
        for c in current:
            if c not in areas:
                employee.powerDown(c, IWorkLocations)
                c.powerDown(employee, IEmployee)
        for a in areas:
            if a not in current:
                employee.powerUp(a, IWorkLocations)
                a.powerUp(employee, IWorkLocations)
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
