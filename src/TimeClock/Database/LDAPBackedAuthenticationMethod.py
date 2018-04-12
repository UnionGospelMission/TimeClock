from zope.interface import implementer

import twisted
import twisted.internet.defer
from TimeClock import AD
from TimeClock.Database.CacheAuthenticationMethod import CacheAuthenticationMethod
from TimeClock.Exceptions import PermissionDenied
from TimeClock.Utils import overload
from axiom.attributes import text, boolean

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IAuthenticationMethod import IAuthenticationMethod
from hashlib import sha512

from twisted.internet import reactor


def getSalt(*_):
    with open('/dev/urandom', 'rb') as f:
        return repr(f.read(512).decode('charmap'))


@implementer(IAuthenticationMethod)
class LDAPBackedAuthenticationMethod(Item):
    @staticmethod
    def hash(pw, salt):
        return str(sha512((pw + salt).encode('charmap')).hexdigest())
    schemaVersion = 1
    password = text()
    salt = text(defaultFactory=getSalt)
    expired = boolean(default=False)

    @classmethod
    def fromCacheAuthenticationMethod(cls, employee: IEmployee, cam: CacheAuthenticationMethod):
        new = cls(salt=cam.salt, password=cam.password, expired=cam.expired, store=cam.store)
        employee.alternate_authentication = new
        return new

    def authenticate(self, employee: IEmployee, password: str) -> bool:
        if self.hash(password, self.salt) == self.password:
            return twisted.internet.defer.succeed(True)
        else:
            if employee.active_directory_name:
                d = twisted.internet.threads.deferToThread(self._authenticate, employee.active_directory_name, password)
                d.addCallback(lambda valid: (self.setPassword(password) or True) if valid else False)
                return d
            d = twisted.Deferred()
            reactor.callLater(2, d.callback, False)
            return d

    def _authenticate(self, adn, pw):
        return AD.authenticate(adn, pw)

    def expire(self):
        import twisted.internet.reactor as reactor
        reactor.callFromThread(self._expire)

    def _expire(self):
        self.expired = True

    @overload
    def setPassword(self, pw):
        newpw = str(sha512((pw + self.salt).encode('charmap')).hexdigest())
        self.password = newpw
        self.expired = False
        return self

    @overload
    def setPassword(self, employee: IEmployee, pw: str):
        valid = AD.authenticate(employee.active_directory_name, pw)
        if valid:
            self.setPassword(pw)
            return self
        else:
            raise PermissionDenied("Incorrect old password")

