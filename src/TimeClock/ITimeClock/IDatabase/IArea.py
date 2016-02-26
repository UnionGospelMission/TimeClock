from twisted.python.components import registerAdapter
from zope.interface import Attribute, Interface

from TimeClock.Axiom.Store import Store
from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.Util import Null
from TimeClock.Utils import coerce, overload


class IAbstractArea(IItem):
    name = Attribute("name")
    sub = Attribute("sub")


class IArea(IAbstractArea):
    from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee

    def getEmployees() -> [IEmployee]:
        pass

    def addEmployee(employee: IEmployee):
        pass
    del IEmployee


@coerce
def newArea(_) -> IArea:
    from ...Database.Area import Area
    return Area(store=Store)


@overload
def findArea(s: int) -> IArea:
    from ...Database.Area import Area
    ret = list(Store.query(Area, Area.sub == s))
    if ret:
        return ret[0]


@overload
def findArea(s: str) -> IArea:
    from ...Database.Area import Area
    ret = list(Store.query(Area, Area.name == s))
    if ret:
        return ret[0]

registerAdapter(newArea, Null, IArea)
registerAdapter(findArea, str, IArea)
registerAdapter(findArea, int, IArea)
