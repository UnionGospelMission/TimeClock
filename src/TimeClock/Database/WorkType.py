from twisted.python.components import registerAdapter

from TimeClock.Axiom.Store import Store
from TimeClock.Util import Null
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation


@implementer(IWorkLocation)
class WorkType(Item):
    workLocationID = text()
    description = text()


def findWorkType(i):
    return Store.findFirst(WorkType, WorkType.workLocationID == i)

registerAdapter(findWorkType, str, IWorkLocation)
registerAdapter(lambda x: WorkType(store=Store), Null, IWorkLocation)
