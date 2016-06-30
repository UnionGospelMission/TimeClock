from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.IEvent.IWebEvent.ISupervisorCreatedRemovedEvent import ISupervisorCreatedRemovedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(ISupervisorCreatedRemovedEvent)
class SupervisorRemovedEvent(WebEvent):
    @coerce
    def __init__(self, e: IEmployee, s: ISupervisor):
        self.employee = e
        self.supervisor = s
    def getType(self):
        return ISupervisorCreatedRemovedEvent
