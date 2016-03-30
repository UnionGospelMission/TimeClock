from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ILogger import ILogger
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Solomon import Solomon
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
def findSubAccount(s: int) -> ISubAccount:
    from TimeClock.Axiom.Store import Store
    ret = list(Store.query(SubAccount, SubAccount.sub == s))
    if ret:
        return ret[0]
    r = Solomon.getSubAccount(s)
    return Store.findOrCreate(SubAccount, sub=s, name=r['Descr'])

@overload
def findSubAccount(s: str) -> ISubAccount:
    if s.strip().isdigit():
        import traceback
        stack = traceback.format_stack()
        ILogger("Database").warn("findSubAccount(str) called with numeric string, caller should cast to int" +
                                 str.join('\n', stack))
        return findSubAccount(int(s))
    from TimeClock.Axiom.Store import Store
    ret = list(Store.query(SubAccount, SubAccount.name == s))
    if ret:
        return ret[0]
    r = Solomon.getSubAccount(s)
    if r:
        return Store.findOrCreate(SubAccount, name=s, sub=r['Sub'])

registerAdapter(newArea, Null, ISubAccount)
registerAdapter(findSubAccount, str, ISubAccount)
registerAdapter(findSubAccount, int, ISubAccount)
