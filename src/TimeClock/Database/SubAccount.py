from twisted.python.components import registerAdapter
from zope.interface import implementer


from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Util import Null
from TimeClock.Utils import coerce, overload
from axiom.attributes import text, integer
from axiom.item import Item


@implementer(ISubAccount)
class SubAccount(Item):
    name = text()
    sub = integer()
    def getEmployees(self) -> [IEmployee]:
        return self.powerupsFor(IEmployee)
    def addEmployee(self, employee: IEmployee):
        employee.powerUp(self, ISubAccount)
        self.powerUp(employee, IEmployee)


@coerce
def newArea(_) -> ISubAccount:
    from TimeClock.Axiom.Store import Store
    return SubAccount(store=Store)


@overload
def findArea(s: int) -> ISubAccount:
    from TimeClock.Axiom.Store import Store
    ret = list(Store.query(SubAccount, SubAccount.sub == s))
    if ret:
        return ret[0]

@overload
def findArea(s: str) -> ISubAccount:
    from TimeClock.Axiom.Store import Store
    ret = list(Store.query(SubAccount, SubAccount.name == s))
    if ret:
        return ret[0]

registerAdapter(newArea, Null, ISubAccount)
registerAdapter(findArea, str, ISubAccount)
registerAdapter(findArea, int, ISubAccount)
