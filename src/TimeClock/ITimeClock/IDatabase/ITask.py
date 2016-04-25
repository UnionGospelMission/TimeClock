from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class ITask(IItem):
    name = Attribute("name")
    description = Attribute("description")
    expected_hours = Attribute("expected_hours")
