from twisted.python.components import registerAdapter
from zope.interface import implementer
from TimeClock.ITimeClock.IDateTime import IDateTime, ITimeDelta

from TimeClock.Axiom.Attributes import datetime
from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import Null
from TimeClock.Utils import overload, coerce
from axiom.item import Item

import time


@implementer(ITimePeriod)
class TimePeriod(Item):
    _startTime = datetime()
    _endTime = datetime()

    @overload
    def start(self):
        self._startTime = time.time()
    @overload
    def start(self, t: float):
        self._startTime = t
    @overload
    def start(self, t: IDateTime):
        self._startTime = t
    @overload
    def end(self):
        self._endTime = time.time()
    @overload
    def end(self, t: float):
        self._endTime = t
    @overload
    def end(self, t: IDateTime):
        self._endTime = t

    @coerce
    def startTime(self) -> IDateTime:
        return self._startTime

    @coerce
    def endTime(self, now: bool=True) -> IDateTime:
        if now:
            return self._endTime or time.time()
        return self._endTime

    def duration(self) -> ITimeDelta:
        et = self.endTime()
        return et - self.startTime()


@overload
def newTimePeriod(n: Null) -> ITimePeriod:
    tp = TimePeriod(store=Store.Store)
    tp._startTime = time.time()
    return tp


@overload
def newTimePeriod(n: float) -> ITimePeriod:
    tp = TimePeriod(store=Store.Store)
    tp._startTime = n
    return tp


registerAdapter(newTimePeriod, Null, ITimePeriod)
registerAdapter(newTimePeriod, float, ITimePeriod)
