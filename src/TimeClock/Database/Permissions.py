from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.attributes import text
from axiom.item import Item
from ..ITimeClock.IDatabase.IPermission import IPermission


@implementer(IPermission, IItem)
class Permission(Item):
    name = text()

