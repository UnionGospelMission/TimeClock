from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IPermission(IItem):
    name = Attribute("name")
