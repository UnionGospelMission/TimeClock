from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IFile(IItem):
    path = Attribute("path")
