from zope.interface import implementer
from axiom.attributes import text

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IAuthenticationMethod import IAuthenticationMethod
from hashlib import sha512


def getSalt(*args):
    with open('/dev/urandom', 'rb') as f:
        return repr(f.read(512).decode('charmap'))


@implementer(IAuthenticationMethod)
class StaticAuthenticationMethod(Item):
    password = text()
    salt = text(defaultFactory=getSalt)
    def authenticate(self, employee: IEmployee, password: str) -> bool:
        return str(sha512((password + self.salt).encode('charmap')).hexdigest()) == self.password
    def setPassword(self, pw):
        newpw = str(sha512((pw + self.salt).encode('charmap')).hexdigest())
        self.password = newpw
        return self
