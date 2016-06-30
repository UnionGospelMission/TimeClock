from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaExpandable import IAthenaExpandable
from TimeClock.Web.LiveFragment import LiveFragment


@implementer(IAthenaExpandable)
class AbstractExpandable(object):
    expanded = True

    def expand(self):
        self.expanded = True
        self.callRemote('expand')

    def shrink(self):
        self.expanded = False
        self.callRemote('shrink')
