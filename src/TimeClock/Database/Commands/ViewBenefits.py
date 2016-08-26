from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from axiom.item import Item

from axiom.attributes import text
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Utils import overload


@implementer(ICommand, IItem)
class ViewBenefits(Item):
    name = text(default='View Benefits')
    @overload
    def hasPermission(self, permissions: [IPermission]) -> bool:
        return True
    @overload
    def hasPermission(self, *a) -> bool:
        return True
    @overload
    def execute(self, caller: IPerson):
        pass
    @overload
    def execute(self, caller: IPerson, *parameters: object):
        print(44, caller, parameters)
        raise NotImplementedError("%s called with invalid parameters" % self.name)
