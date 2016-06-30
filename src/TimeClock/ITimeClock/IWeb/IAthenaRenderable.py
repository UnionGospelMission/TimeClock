from zope.interface import Interface, Attribute

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Web.LiveFragment import LiveFragment
from nevow import inevow


class IAthenaRenderable(inevow.IRenderer):
    def prepare(parent: LiveFragment):
        pass
    employee = Attribute("employee")
