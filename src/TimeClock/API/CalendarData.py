from twisted.python.components import registerAdapter
from zope.interface import implementer
from TimeClock.ITimeClock.IDateTime import ITimeDelta


from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.Utils import overload, coerce


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
        if not self.entries:
            return
        return self.entries[0].startTime()

    def endTime(self) -> IDateTime:
        if not self.entries:
            return
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

    def between(self, start: IDateTime, end: IDateTime) -> ICalendarData:
        o = []
        for i in self.entries:
            et = i.endTime()
            st = i.startTime()
            if start and et and start > et:
                continue
            if end and st and end < st:
                continue
            o.append(i)
        return CalendarData(o)
    @coerce
    def sumBetween(self, start: IDateTime, end: IDateTime) -> ITimeDelta:
        b = self.between(start, end)
        total = start - start
        all = iter(b.allTimes())
        for st in all:
            et = next(all)
            if st < start:
                st = start
            if et > end:
                et = end
            this = et - st
            total += this
        return total
    @coerce
    def getData(self, date: IDateTime):
        start = date.date()
        end = date.date().replace(days=1)
        return "%0.2f" % (self.sumBetween(start, end).seconds / 60 / 60)
    def addTime(self, dt: IDateTime):
        self.entries.append(dt)
        self.entries.sort(key=lambda x: x.startTime())









registerAdapter(CalendarData, list, ICalendarData)
registerAdapter(CalendarData, tuple, ICalendarData)
registerAdapter(CalendarData, ITimePeriod, ICalendarData)
