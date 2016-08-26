from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.Utils import overload
from axiom.item import Item

from axiom.attributes import text


@implementer(ICommand, IItem)
class ManageWorkLocations(Item):
    name = text()

    @overload
    def hasPermission(self, caller: IPerson) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("Dummy command for permission checking only" % self.name)
