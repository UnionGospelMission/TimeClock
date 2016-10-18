from TimeClock.Util.registerAdapter import adapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.IBenefit import IBenefit
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType
from TimeClock.Report.IAccess.IABenefit import IABenefit
from TimeClock.Utils import coerce


@adapter(IBenefit, IABenefit)
@implementer(IABenefit)
class ABenefit(object):
    __slots__ = ['_benefit']

    @coerce
    def __init__(self, _benefit: IBenefit):
        self._benefit = _benefit

    @property
    def code(self):
        return self._benefit.code

    @property
    def classId(self):
        return self._benefit.classId

    @property
    def description(self):
        return self._benefit.description


