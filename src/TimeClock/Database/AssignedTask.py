from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.IAssignedTask import IAssignedTask
from TimeClock.Util import Null
from axiom.item import Item

from axiom.attributes import point2decimal, text

from axiom.attributes import boolean, reference


@implementer(IAssignedTask)
class AssignedTask(Item):
    task = reference()
    employee = reference()
    completed = boolean(default=False)
    time_taken = point2decimal()
    notes = text()

registerAdapter((lambda n: AssignedTask(store=Store.Store)), Null, IAssignedTask)
