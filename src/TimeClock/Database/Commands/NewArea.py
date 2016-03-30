from zope.interface import Attribute, implementer, Interface

import TimeClock
from TimeClock.Exceptions import PermissionDenied, InvalidTransformation
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.Util import NULL
from TimeClock.Utils import coerce, overload
from axiom.item import Item
from axiom.attributes import text


@implementer(ICommand, IItem)
class NewArea(Item):
    name = text()
    @coerce
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return TimeClock.API.Permissions.NewArea in permissions
    @overload
    def execute(self, caller: IPerson, name: str, sub: int):
        if self.hasPermission(caller.getPermissions()):
            area = ISubAccount(name, None)
            if not area:
                area = ISubAccount(NULL)
                area.name = name
                area.sub = sub
                return area
            else:
                raise InvalidTransformation("SubAccount named %s already exists"%name)
        raise PermissionDenied()
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)
