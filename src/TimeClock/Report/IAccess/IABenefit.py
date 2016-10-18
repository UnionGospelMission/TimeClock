from zope.interface import Attribute

from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IABenefit(IAbstractAccessible):
    code = Attribute("code")
    classId = Attribute("classId")
    description = Attribute("description")
