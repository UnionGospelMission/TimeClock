from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class ILogEntry(IItem):
    level = Attribute("level")
    message = Attribute("message")
    logger = Attribute("logger")
