
from .Util.Coerce import Coercer
from .Util.Overload import Overloader
from .Util import fromFunction
from .Util.subclass import issubclass, Subclass

def coerce(func):
    return Coercer(func)


def overload(func):
    return Overloader().add(func)


@coerce
def getAllEmployees() -> list:
    from TimeClock.Axiom.Store import Store
    from TimeClock.Database.Employee import Employee
    return Store.query(Employee)

TZOffsets = dict(
    PST=-480,
    PDT=-420,
    CDT=-300,
    CST=-360,
    EDT=-240,
    EST=-300,
    MDT=-360,
    MST=-420,
    AKDT=-480,
    AKST=-540,
    HADT=-540,
    HAST=-600
)
