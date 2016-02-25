from twisted.python.components import registerAdapter
from zope.interface import implementer
from zope.interface.common.idatetime import IDateTime

from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Utils import overload


@implementer(ICalendarData)
class CalendarData(object):
    @overload
    def __init__(self, entries: list):
        self.entries = entries
        self.entries.sort(key=lambda x: x.startTime())

    @overload
    def __init__(self, entry: ITimePeriod):
        self.__init__([entry])

    def startTime(self) -> IDateTime:
        return self.entries[0].startTime()

    def endTime(self) -> IDateTime:
        return self.entries[-1].endTime()

    def __iter__(self) -> [ITimePeriod]:
        return iter(self.entries)

    def startTimes(self) -> [IDateTime]:
        return [i.startTime() for i in self.entries]

    def endTimes(self) -> [IDateTime]:
        return [i.endTime() for i in self.entries]

    def allTimes(self) -> [IDateTime]:
        for i in self.entries:
            yield i.startTime()
            yield i.endTime()


registerAdapter(CalendarData, list, ICalendarData)
registerAdapter(CalendarData, tuple, ICalendarData)
registerAdapter(CalendarData, ITimePeriod, ICalendarData)
