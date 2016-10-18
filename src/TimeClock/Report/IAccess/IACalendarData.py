from zope.interface.common.idatetime import ITimeDelta

from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.Report.IAccess.IATimeEntry import IATimeEntry
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible


class IACalendarData(IAbstractAccessible):
    """
    Collection of {ATimeEntry}s
    """
    def startTime() -> IDateTime:
        """Returns the start time of the first entry"""

    def endTime() -> IDateTime:
        """
        Returns the end time of the last entry
        """

    def __iter__() -> [IATimeEntry]:
        """
        Iterates over all entries
        """

    def startTimes() -> [IDateTime]:
        """
        Returns the list of start times of all entries
        """

    def endTimes() -> [IDateTime]:
        """
        Returns the list of end times of all entries
        """

    def allTimes() -> [IDateTime]:
        """
        Returns startTime_0, endTime_0, startTime_1 ... endTime_n
        """

    def between(start: IDateTime, end: IDateTime):
        """
        Returns all entries between start and end, entries which extend beyond start or end are truncated
        """

    def getData(date: IDateTime) -> str:
        """
        Returns the number of hours worked on a given date
        """

    def sumBetween(start: IDateTime, end: IDateTime) -> ITimeDelta:
        """
        Returns {ITimeDelta} for the number of hours worked
        """

IACalendarData['between'].annotations['return'] = IACalendarData


