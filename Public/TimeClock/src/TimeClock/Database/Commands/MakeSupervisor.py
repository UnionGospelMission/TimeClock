from zope.interface import implementer

from TimeClock.Database import Permissions
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from axiom.item import Item
from TimeClock.Database import Supervisor


@implementer(ICommand, IItem)
class MakeSupervisor(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]):
        return Permissions.MakeSupervisor in permissions
    @overload
    def execute(self, caller: IEmployee, employee: IEmployee):
        if self.hasPermission(caller.getPermissions()):
            s = ISupervisor(employee, None)
            if s is None:
                s = ISupervisor(NULL)
                employee.powerUp(s, ISupervisor)
                s.employee = employee
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        print(32, self, caller, parameters, sep='\n')
        raise NotImplementedError("%s called with invalid parameters"%self.name)
