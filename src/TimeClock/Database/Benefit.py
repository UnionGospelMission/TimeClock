from twisted.python.components import registerAdapter

from TimeClock.Axiom.Store import Store
from TimeClock.Util import Null
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
    return Store.findFirst(Benefit, Benefit.code == code)


def findOrCreateBenefit(benentry: dict) -> IBenefit:
    return Store.findOrCreate(Benefit, code=benentry['BenId'], classId=benentry['ClassId'], description=benentry['Descr'])


registerAdapter(findBenefit, str, IBenefit)
registerAdapter(lambda _: Benefit(store=Store), Null, IBenefit)
registerAdapter(findOrCreateBenefit, dict, IBenefit)
