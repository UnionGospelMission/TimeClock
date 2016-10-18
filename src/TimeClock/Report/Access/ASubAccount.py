from TimeClock.Util.registerAdapter import adapter
from TimeClock.Utils import coerce
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.Report.IAccess.IASubAccount import IASubAccount


@adapter(ISubAccount, IASubAccount)
@implementer(IASubAccount)
class ASubAccount(object):
    __slots__ = ['_subAccount']

    @coerce
    def __init__(self, sa: ISubAccount):
        self._subAccount = sa

    @property
    def name(self):
        return self._subAccount.name

    @property
    def active(self):
        return self._subAccount.active

    @property
    def sub(self):
        return self._subAccount.sub

