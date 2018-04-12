from zope.interface import implementer
import ldap3
from TimeClock import AD
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
class CacheAuthenticationMethod(Item):
    schemaVersion = 2
    password = text()
    salt = text(defaultFactory=getSalt)
    expired = boolean(default=False)

    def authenticate(self, employee: IEmployee, password: str) -> bool:
        if employee.active_directory_name:
            from TimeClock.Database.LDAPBackedAuthenticationMethod import LDAPBackedAuthenticationMethod
            return LDAPBackedAuthenticationMethod.fromCacheAuthenticationMethod(employee, self).authenticate(employee, password)
            # try:
            #     valid = AD.authenticate(employee.active_directory_name, password)
            #     if valid:
            #         newpw = str(sha512((password + self.salt).encode('charmap')).hexdigest())
            #         if self.password != newpw:
            #             self.password = newpw
            #     return valid
            # except ldap3.core.exceptions.LDAPException:
            #     return str(sha512((password + self.salt).encode('charmap')).hexdigest()) == self.password
        else:
            return str(sha512((password + self.salt).encode('charmap')).hexdigest()) == self.password

    def setPassword(self, pw):
        newpw = str(sha512((pw + self.salt).encode('charmap')).hexdigest())
        self.password = newpw
        self.expired = False
        return self

registerAttributeCopyingUpgrader(
    CacheAuthenticationMethod,
    1,
    2
)
