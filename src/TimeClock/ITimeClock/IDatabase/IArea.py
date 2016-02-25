from twisted.python.components import registerAdapter
from zope.interface import Attribute, Interface

from TimeClock.Axiom.Store import Store
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.Util import Null
from TimeClock.Utils import coerce


class IAbstractArea(IItem):
    name = Attribute("name")


import TimeClock.ITimeClock.IDatabase.IEmployee
class IArea(IAbstractArea):
    def getEmployees() -> [TimeClock.ITimeClock.IDatabase.IEmployee.IEmployee]:
        pass
    def addEmployee(employee: TimeClock.ITimeClock.IDatabase.IEmployee.IEmployee):
        pass

@coerce
def newArea(x) -> IArea:
    from ...Database.Area import Area
    return Area(store=Store)

@coerce
def findArea(s: str) -> IArea:
    from ...Database.Area import Area
    ret = list(Store.query(Area, Area.name==s))
    if ret:
        return ret[0]

registerAdapter(newArea, Null, IArea)
registerAdapter(findArea, str, IArea)
