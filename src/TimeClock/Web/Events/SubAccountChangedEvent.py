from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IEvent.IWebEvent.ISubAccountChangedEvent import ISubAccountChangedEvent
from TimeClock.Utils import coerce
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(ISubAccountChangedEvent)
class SubAccountChangedEvent(WebEvent):
    @coerce
    def __init__(self, sa: ISubAccount, previous_values):
        self.subAccount = sa
        self.previous_values = previous_values
    def getType(self):
        return ISubAccountChangedEvent
