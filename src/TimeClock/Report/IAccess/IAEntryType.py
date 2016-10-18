from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.Report.IAccess.IABenefit import IABenefit
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IAEntryType(IAbstractAccessible):
    id = Attribute('id')

    def getDescription() -> str:
        """
        Returns the human readable description
        """

    def getTypeName() -> str:
        """
        Returns the entry type name
        """

    def getBenefit() -> IABenefit:
        """
        Returns the benefit type associated with this entry type
        """
