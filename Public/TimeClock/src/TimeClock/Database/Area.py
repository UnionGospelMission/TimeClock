from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IArea import IArea
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from axiom.attributes import text
from axiom.item import Item


@implementer(IArea)
class Area(Item):
    name = text()
    def getEmployees(self) -> [IEmployee]:
        return self.powerupsFor(IEmployee)
    def addEmployee(self, employee: IEmployee):
        employee.powerUp(self, IArea)
        self.powerUp(employee, IEmployee)
