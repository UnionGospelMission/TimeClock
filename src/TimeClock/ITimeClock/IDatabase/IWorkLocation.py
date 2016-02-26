from TimeClock.ITimeClock.IDatabase.IItem import IItem
from epsilon.descriptor import attribute


class IWorkLocation(IItem):
    workLocationID = attribute("id")
    description = attribute("description")
