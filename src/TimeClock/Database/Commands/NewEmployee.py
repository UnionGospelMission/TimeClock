from zope.interface import Attribute, implementer, Interface

from TimeClock.Database import Permissions
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.Util import NULL
from TimeClock.Util.subclass import Subclass
from TimeClock.Utils import coerce, overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class NewEmployee(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]):
        return Permissions.NewEmployee in permissions
    @overload
    def execute(self, caller: IEmployee, eid: int, **kw:object):
        if self.hasPermission(caller.getPermissions()):
            e = IEmployee(NULL)
            e.employee_id = eid
            for k,v in kw.items():
                setattr(e,k,v)
            return e
        raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
