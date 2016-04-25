from TimeClock.ITimeClock.IDatabase.IItem import IItem
from zope.interface import Attribute

from TimeClock.Util import fromFunction


class IWorkLocation(IItem):
    workLocationID = Attribute("id")
    description = Attribute("description")
    active = Attribute("active")

    @fromFunction
    def getEmployees() -> "":
        pass
