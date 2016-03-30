import time
from zope.interface import implementer
from TimeClock.ITimeClock.IDateTime import ITimeDelta

from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.Util import fromFunction
from TimeClock.Utils import overload, coerce


@implementer(ITimePeriod)
class InMemoryTimePeriod(object):
    _startTime = None
    _endTime = None
    def __init__(self, startTime: IDateTime=None, endTime: IDateTime=None):
        self.start(startTime)
        if endTime:
            self.end(endTime)
    @overload
    def start(self):
        self.start(time.time())
    @overload
    def start(self, t: float):
        self._startTime = IDateTime(t)
    @overload
    def start(self, t: IDateTime):
        self._startTime = t
    @overload
    def end(self):
        self.end(time.time())
    @overload
    def end(self, t: float):
        self.end(IDateTime(t))
    @overload
    def end(self, t: IDateTime):
        self._endTime = t

    @coerce
    def startTime(self) -> IDateTime:
        return self._startTime

    @coerce
    def endTime(self) -> IDateTime:
        return self._endTime or time.time()

    def duration(self) -> ITimeDelta:
        if self.endTime is None:
            et = IDateTime(time.time())
        else:
            et = self.endTime()
        return et - self.startTime()

