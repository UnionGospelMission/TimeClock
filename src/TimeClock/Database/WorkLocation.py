from twisted.python.components import registerAdapter

from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Solomon import Solomon
from TimeClock.Util import Null
from TimeClock.Utils import coerce
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation


@implementer(IWorkLocation)
class WorkLocation(Item):
    workLocationID = text()
    description = text()
    @coerce
    def getEmployees(self) -> [IEmployee]:
        return self.powerupsFor(IEmployee)


def findWorkType(i):
    ret = list(Store.Store.query(WorkLocation, WorkLocation.workLocationID == i))
    if ret:
        return ret[0]
    r = Solomon.getWorkLocation(i)
    return Store.Store.findOrCreate(WorkLocation, workLocationID=i, description=r['Descr'])

registerAdapter(findWorkType, str, IWorkLocation)
registerAdapter(lambda x: WorkLocation(store=Store.Store), Null, IWorkLocation)
