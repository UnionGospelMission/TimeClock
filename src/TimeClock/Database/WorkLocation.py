from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from TimeClock.Util import Null
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation


@implementer(IWorkLocation)
class WorkLocation(Item):
    workLocationID = text()
    description = text()


def findWorkType(i):
    return Store.Store.findFirst(WorkLocation, WorkLocation.workLocationID == i)

registerAdapter(findWorkType, str, IWorkLocation)
registerAdapter(lambda x: WorkLocation(store=Store.Store), Null, IWorkLocation)
