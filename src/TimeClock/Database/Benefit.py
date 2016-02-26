from twisted.python.components import registerAdapter

from TimeClock.Axiom.Store import Store
from TimeClock.Solomon import Solomon
from TimeClock.Util import Null, NULL
from axiom.attributes import text
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from axiom.item import Item


@implementer(IBenefit)
class Benefit(Item):
    code = text()
    classId = text()
    description = text()


def findBenefit(code: str) -> IBenefit:
    s = list(Store.query(Benefit, Benefit.code == code))
    if s:
        return s[0]


def findOrCreateBenefit(benentry: dict) -> IBenefit:
    s = IBenefit(benentry['BenId'], None)
    if not s:
        b = Solomon.getBenefit(benentry['BenId'])
        s = IBenefit(NULL)
        s.code = benentry['BenId']
        s.classId = b['ClassId']
        s.description = b['Descr']
    return s


registerAdapter(findBenefit, str, IBenefit)
registerAdapter(lambda _: Benefit(store=Store), Null, IBenefit)
registerAdapter(findOrCreateBenefit, dict, IBenefit)
