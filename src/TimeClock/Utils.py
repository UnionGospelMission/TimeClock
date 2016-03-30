
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
