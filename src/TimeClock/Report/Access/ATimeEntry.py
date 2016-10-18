from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.ITimeDelta import ITimeDelta
from TimeClock.Report.IAccess.IAEntryType import IAEntryType
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.Report.IAccess.IACalendarData import IACalendarData
from TimeClock.Report.IAccess.IASubAccount import IASubAccount
from TimeClock.Report.IAccess.IATimeEntry import IATimeEntry
from TimeClock.Utils import coerce


@implementer(IATimeEntry)
class ATimeEntry(object):
    __slots__ = ['_entry']

    @coerce
    def __init__(self, entry: ITimeEntry):
        self._entry = entry

    @property
    def startTime(self):
        return self._entry.startTime()

    @property
    def endTime(self):
        return self._entry.endTime(False)

    @property
    @coerce
    def entryType(self) -> IAEntryType:
        return self._entry.type

    @property
    @coerce
    def subAccount(self) -> IASubAccount:
        return self._entry.subAccount

    @property
    @coerce
    def workLocation(self) -> IAWorkLocation:
        return self._entry.workLocation

    @property
    def duration(self):
        return self._entry.duration()

    @property
    def approved(self):
        return self._entry.approved

    @property
    def denied(self):
        return self._entry.denied

    @coerce
    def truncate(self, startTime: IDateTime, endTime: IDateTime) -> ITimeDelta:
        return IACalendarData(self._entry).sumBetween(startTime, endTime)

registerAdapter(ATimeEntry, ITimeEntry, IATimeEntry)
