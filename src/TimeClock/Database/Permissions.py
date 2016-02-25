from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IItem import IItem
from axiom.attributes import text
from axiom.item import Item
from ..Axiom.Store import Store
from ..ITimeClock.IDatabase.IPermission import IPermission


@implementer(IPermission, IItem)
class Permission(Item):
    name = text()

MakeSupervisor = Store.findOrCreate(Permission, name="Make Supervisor")
NewEmployee = Store.findOrCreate(Permission, name="New Employee")
ClockIn = Store.findOrCreate(Permission, name="Clock In")
NewArea = Store.findOrCreate(Permission, name="New Area")
AssignArea = Store.findOrCreate(Permission, name="Assign Area")
