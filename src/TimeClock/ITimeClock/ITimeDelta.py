from twisted.python.components import registerAdapter
from zope.interface.common.idatetime import ITimeDelta as itd
from datetime import timedelta


class ITimeDelta(itd):
    def total_seconds() -> float:
        pass


registerAdapter(timedelta, float, ITimeDelta)
registerAdapter(timedelta, int, ITimeDelta)
