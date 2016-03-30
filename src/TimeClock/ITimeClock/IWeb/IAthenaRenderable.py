from zope.interface import Interface

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Web.LiveFragment import LiveFragment
from nevow import inevow


class IAthenaRenderable(inevow.IRenderer):
    def prepare(parent: LiveFragment):
        pass
