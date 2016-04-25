from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Utils import overload
from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IItem import IItem


@implementer(ICommand, IItem)
class ViewReports(Item):
    name = text()
    @overload
    def hasPermission(self, caller: IEmployee) -> bool:
        return self.hasPermission(caller.getPermissions())

    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    def execute(self, caller: IPerson):
        pass
