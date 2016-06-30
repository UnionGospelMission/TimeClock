from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IEvent.IWebEvent.IEmployeeChangedEvent import IEmployeeChangedEvent
from TimeClock.ITimeClock.IEvent.IWebEvent.ISubAccountChangedEvent import ISubAccountChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(IEmployeeChangedEvent)
class SubAccountAssignmentChangedEvent(WebEvent):
    @coerce
    def __init__(self, e: IEmployee, previous_values):
        self.employee = e
        self.previous_values = previous_values
    def getType(self):
        return IEmployeeChangedEvent
