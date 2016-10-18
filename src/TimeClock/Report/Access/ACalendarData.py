from zope.interface import implementer
from zope.interface.common.idatetime import ITimeDelta

from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.ITimePeriod import ITimePeriod
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.Report.IAccess import IACalendarData, IATimeEntry
from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import i_coerce, coerce


@adapter(ICalendarData, IACalendarData)
@adapter(list, IACalendarData)
@adapter(tuple, IACalendarData)
@adapter(ITimePeriod, IACalendarData)
@implementer(IACalendarData)
class ACalendarData(object):
    __slots__ = ['_calendarData']

    @coerce
    def __init__(self, cd: ICalendarData):
        self._calendarData = cd

    def startTime(self) -> IDateTime:
        return self._calendarData.startTime()

    def endTime(self) -> IDateTime:
        return self._calendarData.endTime()

    def __iter__(self) -> IATimeEntry:
        for i in self._calendarData:
            yield IATimeEntry(i)

    def startTimes(self) -> [IDateTime]:
        return self._calendarData.startTimes()

    def endTimes(self) -> [IDateTime]:
        return self._calendarData.endTimes()

    def allTimes(self) -> [IDateTime]:
        return self._calendarData.allTimes()

    def between(self, start: IDateTime, end: IDateTime):
        return self._calendarData.between(start=start, end=end)

    def getData(self, date: IDateTime):
        return self._calendarData.getData(date=date)

    def sumBetween(self, start: IDateTime, end: IDateTime) -> ITimeDelta:
        return self._calendarData.sumBetween(start=start, end=end)

