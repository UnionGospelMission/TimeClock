from twisted.python.components import registerAdapter

from TimeClock.Axiom.Store import Store
from axiom.attributes import text

from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from axiom.item import Item
from zope.interface import implementer


@implementer(IEntryType)
class EntryType(Item):
    name = text()
    def getTypeName(self) -> str:
        return self.name


def findEntry(s):
    return Store.findOrCreate(EntryType, name=s)


registerAdapter(findEntry, str, IEntryType)
