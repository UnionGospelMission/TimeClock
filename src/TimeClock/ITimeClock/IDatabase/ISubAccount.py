from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IAbstractArea(IItem):
    name = Attribute("name")
    sub = Attribute("sub")


class ISubAccount(IAbstractArea):
    from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee

    def getEmployees() -> [IEmployee]:
        pass

    def addEmployee(employee: IEmployee):
        pass
    del IEmployee

