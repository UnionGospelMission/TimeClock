from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IAssignedTask import IAssignedTask
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ITask import ITask
from TimeClock.Util import NULL
from TimeClock.Utils import overload
from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.item import Item


@implementer(ICommand, IItem)
class CreateTask(Item):
    name = text(default="Create Task")
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return IPermission("Create Task") in permissions
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, name: str, description: str, hours: float):
        if not self.hasPermission(caller.getPermissions()) and not IAdministrator(caller):
            raise PermissionDenied()
        task = ITask(NULL)
        task.name = name
        task.description = description
        task.expected_hours = hours
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(42, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
