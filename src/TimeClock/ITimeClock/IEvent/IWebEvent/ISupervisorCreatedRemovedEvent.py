from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class ISupervisorCreatedRemovedEvent(IWebEvent):
    employee = Attribute("employee")
    supervisor = Attribute("supervisor")
