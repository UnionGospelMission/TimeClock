from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer
from nevow.athena import expose


class AbstractCommandRenderer(AbstractRenderer):
    def render_class(self, *a):
        return self.name.replace(' ', '')
    @expose
    def load(self):
        return

from . import ManageSubAccounts
from . import SetSubAccounts
from . import SetWorkLocations
from . import ManageWorkLocations
from . import ClockInOut
from . import SetSupervisors
from . import ViewEmployees
from . import ViewShifts
from . import ApproveShifts
from . import ViewReports
from . import ScheduleTimeOff
from . import CheckForNewEmployees
from . import SetPassword
# from . import ApproveTimeOff
from . import ViewBenefits
