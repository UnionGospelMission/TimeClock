from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class ITaskChangedEvent(IWebEvent):
    task = Attribute("task")
