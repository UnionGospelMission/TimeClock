from TimeClock.ITimeClock.IDatabase.IItem import IItem
from epsilon.descriptor import attribute


class IWorkLocation(IItem):
    id = attribute("id")
    description = attribute("description")
