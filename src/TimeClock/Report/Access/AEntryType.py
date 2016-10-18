from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.Report.IAccess.IABenefit import IABenefit
from TimeClock.Report.IAccess.IAEntryType import IAEntryType
from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import coerce


@adapter(IEntryType, IAEntryType)
@implementer(IAEntryType)
class AEntryType(object):
    __slots__ = ['_entry']

    @coerce
    def __init__(self, entry: IEntryType):
        self._entry = entry

    def getDescription(self) -> str:
        return self._entry.getDescription()

    def getTypeName(self) -> str:
        return self._entry.getTypeName()

    @coerce
    def getBenefit(self) -> IABenefit:
        return self._entry.getBenefit()

    @property
    def id(self):
        return self._entry.id
