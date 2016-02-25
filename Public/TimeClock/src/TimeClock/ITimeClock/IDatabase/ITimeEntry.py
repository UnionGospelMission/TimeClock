from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from .ITimePeriod import ITimePeriod
from .IArea import IAbstractArea
from .IEntryType import IEntryType


class ITimeEntry(IItem):
    area = Attribute("area")
    type = Attribute("type")
    approved = Attribute("approved")
    period = Attribute("period")

