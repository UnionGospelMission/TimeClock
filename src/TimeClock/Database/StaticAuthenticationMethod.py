from axiom.attributes import bytes as bytes_
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.IAuthenticationMethod import IAuthenticationMethod


@implementer(IAuthenticationMethod)
class StaticAuthenticationMethod(Item):
    password = bytes_()
    def authenticate(self, employee: IEmployee, password: bytes) -> bool:
        return password == self.password
