from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IAssignedTask(IItem):
    task = Attribute("task")
    employee = Attribute("employee")
    completed = Attribute("completed")
    time_taken = Attribute("time_taken")
    notes = Attribute("notes")
