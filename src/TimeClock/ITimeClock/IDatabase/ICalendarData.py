from zope.interface import Interface
from zope.interface.common.idatetime import IDateTime

from .ITimePeriod import ITimePeriod


class ICalendarData(Interface):
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



