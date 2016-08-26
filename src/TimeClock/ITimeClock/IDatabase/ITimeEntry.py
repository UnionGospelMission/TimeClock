from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod


class ITimeEntry(ITimePeriod):
    employee = Attribute("employee")
    subAccount = Attribute("area")
    workLocation = Attribute("workLocation")
    type = Attribute("type")
    approved = Attribute("approved")
    denied = Attribute("denied")
    period = Attribute("period")

