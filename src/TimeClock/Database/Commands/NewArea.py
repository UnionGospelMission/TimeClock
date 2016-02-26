from zope.interface import Attribute, implementer, Interface

from TimeClock.Database import Permissions
from TimeClock.Exceptions import PermissionDenied, InvalidTransformation
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IArea import IArea
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
class NewArea(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]):
        return Permissions.NewArea in permissions
    @overload
    def execute(self, caller: IEmployee, name: str, sub: int):
        if self.hasPermission(caller.getPermissions()):
            print(27, name, sub)
            area = IArea(name, None)
            if not area:
                area = IArea(NULL)
                area.name = name
                area.sub = sub
                return area
            else:
                raise InvalidTransformation("Area named %s already exists"%name)
        raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
