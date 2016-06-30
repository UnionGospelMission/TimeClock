from zope.interface import Attribute

from TimeClock.ITimeClock.IEvent.IWebEvent.IWebEvent import IWebEvent


class ISubAccountChangedEvent(IWebEvent):
    subAccount = Attribute("subAccount")
    previous_values = Attribute("previous_values")
