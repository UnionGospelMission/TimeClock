from twisted.python.components import registerAdapter
from zope.interface.common.idatetime import IDateTime, ITimeDelta

from TimeClock.Axiom.Store import Store
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import Null
from TimeClock.Utils import overload
from axiom.attributes import reference, boolean
from zope.interface import implementer

from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry


@implementer(ITimeEntry, ITimePeriod)
class TimeEntry(Item):
    area = reference()
    workLocation = reference()
    type = reference()
    period = reference()
    approved = boolean(default=False)

    def startTime(self) -> IDateTime:
        return self.period.startTime()

    def endTime(self) -> IDateTime:
        return self.period.endTime()

    @overload
    def start(self):
        self.period.start()

    @overload
    def start(self, t: float):
        self.period.start(t)

    @overload
    def start(self, t: IDateTime):
        self.period.start(t)

    @overload
    def end(self):
        self.period.end()

    @overload
    def end(self, t: float):
        self.period.end(t)

    @overload
    def end(self, t: IDateTime):
        self.period.end(t)

    def duration(self) -> ITimeDelta:
        return self.period.duration()


def newTimeEntry(x):
    te = TimeEntry(store=Store)
    return te

registerAdapter(newTimeEntry, Null, ITimeEntry)
