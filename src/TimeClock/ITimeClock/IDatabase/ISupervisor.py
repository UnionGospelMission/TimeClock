from twisted.python.components import registerAdapter
from zope.interface import Interface, Attribute


from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import fromFunction, Null
from TimeClock.Utils import overload
from .ICalendarData import ICalendarData
from .IEmployee import IEmployee


class ISupervisor(IPerson):
    def getEmployees() -> (IEmployee,):
        pass

    def addEmployee(employee: ISupervisee):
        pass

    # def approveTime(employee: IEmployee, time: ICalendarData):
    #     pass

    # @overload
    # def editTime(employee: IEmployee, time: ICalendarData, affected: ITimePeriod):
    #     pass
    #
    # @fromFunction
    # @overload
    # def editTime(employee: IEmployee, time: ITimePeriod, affected: ITimePeriod):
    #     pass


    employee = Attribute("Employee")

    def getSubAccounts():
        pass



