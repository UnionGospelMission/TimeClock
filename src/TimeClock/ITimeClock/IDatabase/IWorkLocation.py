from TimeClock.ITimeClock.IDatabase.IItem import IItem
from zope.interface import Attribute


class IWorkLocation(IItem):
    workLocationID = Attribute("id")
    description = Attribute("description")
