from zope.interface import Attribute, implementer, Interface

import TimeClock
from TimeClock.Exceptions import PermissionDenied
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class NewEmployee(Item):
    def getArguments(self) -> [object]:
        return ["caller", "Employee ID", "**attributes"]
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return TimeClock.API.Permissions.NewEmployee in permissions
    @overload
    def execute(self, caller: IPerson, eid: int, **kw:object):
        if self.hasPermission(caller.getPermissions()):
            e = IEmployee(NULL)
            e.employee_id = eid
            for k, v in kw.items():
                setattr(e, k, v)
            return e
        else:
            raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
