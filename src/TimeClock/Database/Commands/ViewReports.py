from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IItem import IItem


@implementer(ICommand, IItem)
class ViewReports(Item):
    name = text()
    def hasPermission(self, caller: IPerson) -> bool:
        return True
    def execute(self, caller: IPerson):
        pass
