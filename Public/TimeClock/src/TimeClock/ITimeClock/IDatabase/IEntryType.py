from zope.interface import Interface

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IEntryType(IItem):
    def getTypeName() -> str:
        pass
