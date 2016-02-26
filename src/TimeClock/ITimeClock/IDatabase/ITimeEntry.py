from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class ITimeEntry(IItem):
    area = Attribute("area")
    workLocation = Attribute("workLocation")
    type = Attribute("type")
    approved = Attribute("approved")
    period = Attribute("period")

