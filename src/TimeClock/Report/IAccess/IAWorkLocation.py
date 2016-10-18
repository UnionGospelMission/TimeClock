from zope.interface import Attribute

from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IAWorkLocation(IAbstractAccessible):
    workLocationID = Attribute('workLocationID')
    active = Attribute('active')
    description = Attribute('description')
