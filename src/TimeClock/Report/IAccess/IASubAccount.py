from zope.interface import Attribute

from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IASubAccount(IAbstractAccessible):
    name = Attribute('name')
    active = Attribute('active')
    sub = Attribute('sub')
