from axiom.upgrade import registerAttributeCopyingUpgrader
from twisted.python.components import registerAdapter


from TimeClock.Solomon import Solomon
from TimeClock.Util import Null, NULL
from axiom.attributes import text, boolean
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from axiom.item import Item
import TimeClock



@implementer(IBenefit)
class Benefit(Item):
    schemaVersion = 2
    code = text()
    classId = text()
    description = text()
    active = boolean(default=True)

registerAttributeCopyingUpgrader(
    Benefit,
    1,
    2
)


def findBenefit(code: str) -> IBenefit:
    s = list(TimeClock.Axiom.Store.Store.query(Benefit, Benefit.code == code))
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
registerAdapter(lambda _: Benefit(store=TimeClock.Axiom.Store.Store), Null, IBenefit)
registerAdapter(findOrCreateBenefit, dict, IBenefit)
