from TimeClock.Database.Employee import Employee
from TimeClock.Database.TimePeriod import TimePeriod
from axiom.upgrade import registerAttributeCopyingUpgrader
from twisted.python.components import registerAdapter
from TimeClock.ITimeClock.IDateTime import ITimeDelta

from ..ITimeClock.IDateTime import IDateTime

from TimeClock.Axiom import Store
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Util import Null, NULL
from TimeClock.Utils import overload
from axiom.attributes import reference, boolean
from zope.interface import implementer

from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry


@implementer(ITimeEntry, ITimePeriod)
class TimeEntry(Item):
    subAccount = reference()
    workLocation = reference()
    type = reference()
    period = reference()
    approved = boolean(default=False)
    denied = boolean(default=False)
    employee = reference()

    schemaVersion = 3

    def startTime(self) -> IDateTime:
        return self.period.startTime()

    def endTime(self, now: bool=True) -> IDateTime:
        return self.period.endTime(now)

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

    def getEmployee(self):
        if self.employee is not None:
            return self.employee
        for e in self.store.query(Employee):
            if self in list(e.powerupsFor(ITimeEntry)):
                self.employee = e
                return


registerAttributeCopyingUpgrader(
    TimeEntry,
    1,
    2,
    TimeEntry.getEmployee
)

registerAttributeCopyingUpgrader(
    TimeEntry,
    2,
    3,

)

def newTimeEntry(x):
    te = TimeEntry(store=Store.Store)
    te.period = TimePeriod(store=Store.Store)
    return te

registerAdapter(newTimeEntry, Null, ITimeEntry)
