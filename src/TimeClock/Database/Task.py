from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from TimeClock.Util import Null
from axiom.attributes import text, point2decimal
from zope.interface import implementer

from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.ITask import ITask


@implementer(ITask)
class Task(Item):
    name = text()
    description = text()
    expected_hours = point2decimal()

registerAdapter((lambda n: Task(store=Store.Store)), Null, ITask)
