from zope.interface import Attribute

from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IAbstractSubAccount(IItem):
    name = Attribute("name")
    sub = Attribute("sub")


class ISubAccount(IAbstractSubAccount):
    from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee

    def getEmployees() -> [IEmployee]:
        pass

    def addEmployee(employee: IEmployee):
        pass
    del IEmployee

