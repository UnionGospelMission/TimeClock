from TimeClock.Utils import coerce
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation


@implementer(IAWorkLocation)
class AWorkLocation(object):
    __slots__ = ['_workLocation']

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._workLocation is other._workLocation

    @coerce
    def __init__(self, wl: IWorkLocation):
        self._workLocation = wl

    @property
    def description(self):
        return self._workLocation.description

    @property
    def active(self):
        return self._workLocation.active

    @property
    def workLocationID(self):
        return self._workLocation.workLocationID

    @staticmethod
    def fromID(wid):
        return IAWorkLocation(IWorkLocation(wid))

registerAdapter(AWorkLocation, IWorkLocation, IAWorkLocation)
registerAdapter(AWorkLocation.fromID, str, IAWorkLocation)
