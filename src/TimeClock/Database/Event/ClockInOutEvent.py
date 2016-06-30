from zope.interface import implementer

from TimeClock.Event.AbstractEvent import AbstractEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IDatabaseEvent.ICommandEvent import ICommandEvent
from TimeClock.Utils import coerce


@implementer(IDatabaseEvent)
class ClockInOutEvent(AbstractEvent):
    def getType(self):
        return IDatabaseEvent
    @coerce
    def __init__(self, employee):
        self.employee = employee
        self.clockedIn = bool(employee.timeEntry)

