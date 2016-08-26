from axiom.upgrade import registerAttributeCopyingUpgrader
from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from axiom.attributes import text, boolean

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from axiom.item import Item
from zope.interface import implementer

from TimeClock.Solomon import Solomon


@implementer(IEntryType)
class EntryType(Item):
    schemaVersion = 2
    name = text()
    active = boolean(default=True)
    description = text()
    id = text()
    def getTypeName(self) -> str:
        return self.name
    def getDescription(self) -> str:
        return self.description
    def getBenefit(self) -> IBenefit:
        ben = Solomon.getBenefitByClass(self.name.upper())
        return IBenefit(ben)
    @staticmethod
    def fromSolomon(entry):
        et = IEntryType(entry['BenClassId'])
        if not et.getDescription():
            et.description = entry['Descr']
            et.id = entry['Id']
        return et


registerAttributeCopyingUpgrader(
    EntryType,
    1,
    2
)


def findEntry(s):
    return Store.Store.findOrCreate(EntryType, name=s.title())


registerAdapter(findEntry, str, IEntryType)
registerAdapter(EntryType.fromSolomon, dict, IEntryType)
