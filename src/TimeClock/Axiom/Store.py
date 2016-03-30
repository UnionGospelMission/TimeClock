
from .Attributes import datetime
from axiom import attributes
attributes.datetime = datetime

from .Axiomatic import o
try:
    Store = o.getStore()
except:
    print("Store unavailable, creating testing store")
    from axiom.store import Store as _Store
    Store = _Store()





