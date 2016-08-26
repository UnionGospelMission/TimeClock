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
class AssignTask(Item):
    name = text(default="Assign Task")
    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return IPermission("Assign Task") in permissions
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, task: IAssignedTask):
        if not self.hasPermission(caller.getPermissions()) and not IAdministrator(caller):
            raise PermissionDenied()
        task.employee = employee
        employee.powerUp(task, IAssignedTask)
    @overload
    def execute(self, caller: IPerson, employee: ISupervisee, task: ITask, notes: str):
        if not self.hasPermission(caller.getPermissions()) and not IAdministrator(caller):
            raise PermissionDenied()
        at = IAssignedTask(NULL)
        at.task = task
        at.notes = notes
        at.employee = employee
        employee.powerUp(at, IAssignedTask)
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(42, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
