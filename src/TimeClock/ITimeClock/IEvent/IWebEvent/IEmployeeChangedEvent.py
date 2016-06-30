from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class IEmployeeChangedEvent(IWebEvent):
    employee = Attribute("employee")
    previous_values = Attribute("previous_values")
