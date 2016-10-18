from datetime import timedelta

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.ITimeDelta import ITimeDelta


@implementer(ITimeDelta)
class ATimeDelta(timedelta):
    @classmethod
    def fromTimeDelta(cls, td: timedelta):
        return cls(seconds=td.total_seconds())

    def __add__(self, other):
        return self.fromTimeDelta(super().__add__(other))

    def __sub__(self, other):
        return self.fromTimeDelta(super().__sub__(other))

registerAdapter(ATimeDelta.fromTimeDelta, timedelta, ITimeDelta)
