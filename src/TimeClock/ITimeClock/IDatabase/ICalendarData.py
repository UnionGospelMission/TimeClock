from zope.interface import Interface
from TimeClock.ITimeClock.IDateTime import ITimeDelta


from TimeClock.Util import fromFunction
from TimeClock.Utils import coerce
from .ITimePeriod import ITimePeriod
from ..IDateTime import IDateTime


class ICalendarData(Interface):
    def addTime(dateTime: IDateTime):
        pass

    def startTime() -> IDateTime:
        pass

    def endTime() -> IDateTime:
        pass

    def __iter__() -> [ITimePeriod]:
        pass

    def startTimes() -> [IDateTime]:
        pass

    def endTimes() -> [IDateTime]:
        pass

    def allTimes() -> [IDateTime]:
        pass

    @fromFunction
    def between(start: IDateTime, end: IDateTime):
        """Return a subset of this ICalendarData which starts at or after {start} and ends at or before {end}
        """

    def getData(date: IDateTime):
        pass

    def sumBetween(start: IDateTime, end: IDateTime) -> ITimeDelta:
        pass

ICalendarData['between'].annotations['return'] = ICalendarData


