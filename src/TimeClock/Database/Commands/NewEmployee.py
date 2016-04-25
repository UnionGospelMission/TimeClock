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
    name = text()

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return False
    @overload
    def execute(self, caller: IEmployee, *parameters: object):
        raise NotImplementedError("%s called with invalid parameters" % self.name)

