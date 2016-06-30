from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IEmployeeChangedEvent)
class EmployeeChangedEvent(WebEvent):
    @coerce
    def __init__(self, employee: IEmployee, previous_values):
        self.employee = employee
        self.previous_values = previous_values
    def getType(self):
        return IEmployeeChangedEvent
