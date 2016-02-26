from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IBenefit(IItem):
    code = Attribute("code")
    classId = Attribute("classId")
    description = Attribute("description")
