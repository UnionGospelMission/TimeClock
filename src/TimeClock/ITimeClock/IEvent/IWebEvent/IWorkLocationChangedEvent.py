from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class IWorkLocationChangedEvent(IWebEvent):
    workLocation = Attribute("workLocation")
    previous_values = Attribute("previous_values")
