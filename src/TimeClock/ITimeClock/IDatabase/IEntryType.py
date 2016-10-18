from zope.interface import Interface

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IEntryType(IItem):
    def getDescription() -> str:
        pass

    def getTypeName() -> str:
        pass

    def getBenefit() -> IBenefit:
        pass
