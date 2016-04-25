from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.attributes import text
from axiom.item import Item
from ..ITimeClock.IDatabase.IPermission import IPermission


@implementer(IPermission, IItem)
class Permission(Item):
    name = text()
    @staticmethod
    def findPermission(p):
        return Store.Store.findFirst(Permission, Permission.name == p)


registerAdapter(Permission.findPermission, str, IPermission)
