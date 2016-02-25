from zope.interface import implementer

from TimeClock.Database import Permissions
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.attributes import text
from axiom.item import Item


@implementer(ICommand, IItem)
class ClockIn(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]):
        return Permissions.ClockIn in permissions
    @overload
    def execute(self, caller: IEmployee, area: IArea):
        if self.hasPermission(caller.getPermissions()):
            caller.clockIn(area)
    @overload
    def execute(self, caller: IEmployee, employee: IEmployee, area: IArea):
        if self.hasPermission(caller.getPermissions()):
            employee.clockIn(area)
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters"%self.name)
