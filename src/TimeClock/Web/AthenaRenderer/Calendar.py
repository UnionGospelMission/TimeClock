from zope.interface import implementer
from zope.interface.common.idatetime import IDate

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.LiveFragment import LiveFragment
path =


@implementer(IAthenaRenderable)
class Calendar(LiveFragment):
    startDate = None
    endDate = None
    docFactory =
    def prepare(self, parent: LiveFragment):
        self.parent = parent
        self.setFragmentParent(parent.fragmentParent)
    def setStartDate(self, date: IDate):
        self.startDate = date
    def setEndDate(self, date: IDate):
        self.endDate = date


