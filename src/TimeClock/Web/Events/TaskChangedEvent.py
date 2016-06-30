from zope.interface import implementer

from TimeClock.ITimeClock.IEvent.IWebEvent.ITaskChangedEvent import ITaskChangedEvent
from TimeClock.Web.Events.WebEvent import WebEvent


@implementer(ITaskChangedEvent)
class TaskChangedEvent(WebEvent):
    cancellable = False
    def __init__(self, task):
        self.task = task
    def getType(self):
        return ITaskChangedEvent
