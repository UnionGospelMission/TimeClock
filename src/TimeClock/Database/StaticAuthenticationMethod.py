from zope.interface import implementer

from TimeClock.Database.CacheAuthenticationMethod import CacheAuthenticationMethod
from axiom.attributes import text, boolean

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IAuthenticationMethod import IAuthenticationMethod
from hashlib import sha512

from axiom.upgrade import registerAttributeCopyingUpgrader


def getSalt(*args):
    with open('/dev/urandom', 'rb') as f:
        return repr(f.read(512).decode('charmap'))


@implementer(IAuthenticationMethod)
class StaticAuthenticationMethod(Item):
    schemaVersion = 2
    password = text()
    salt = text(defaultFactory=getSalt)
    expired = boolean(default=True)

    def authenticate(self, employee: IEmployee, password: str) -> bool:
        if employee.active_directory_name:
            na = CacheAuthenticationMethod(store=self.store)
            na.salt = self.salt
            na.password = self.password
            employee.alternate_authentication = na
            return na.authenticate(employee, password)
        return str(sha512((password + self.salt).encode('charmap')).hexdigest()) == self.password

    def setPassword(self, pw):
        newpw = str(sha512((pw + self.salt).encode('charmap')).hexdigest())
        self.password = newpw
        self.expired = False
        return self

registerAttributeCopyingUpgrader(
    StaticAuthenticationMethod,
    1,
    2
)
