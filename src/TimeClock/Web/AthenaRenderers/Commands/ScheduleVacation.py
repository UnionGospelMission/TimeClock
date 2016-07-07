from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom import Transaction
from TimeClock.Database import Commands
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Utils import overload, coerce
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


class ScheduleVacation(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ScheduleVacation'
    subaccounts = None
    name = 'Schedule Vacation'
    def __init__(self, cmd: Commands.ScheduleVacation.ScheduleVacation):
        super().__init__(cmd)
        self.cmd = cmd
    def render_class(self, ctx: WovenContext, data):
        return "ScheduleVacation"
    def render_genericCommand(self, ctx: WovenContext, data):
        startTime = tags.input(id='startTime', type='text', class_='IDateTime', placeholder='Start Time')
        endTime = tags.input(id='endTime', type='text', class_='IDateTime', placeholder='End Time')
        submit = tags.input(type='button', value='Schedule Vacation')[tags.Tag('athena:handler')(event='onclick', handler='scheduleVacation')]
        return self.preprocess([startTime, endTime, submit])
    @expose
    @Transaction
    def scheduleVacation(self, startTime, endTime):
        self.cmd.execute(self.employee, IDateTime(startTime), IDateTime(endTime))


registerAdapter(ScheduleVacation, Commands.ScheduleVacation.ScheduleVacation, IAthenaRenderable)
