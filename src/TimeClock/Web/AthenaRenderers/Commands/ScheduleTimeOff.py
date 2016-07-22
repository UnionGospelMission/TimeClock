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


class ScheduleTimeOff(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ScheduleTimeOff'
    subaccounts = None
    name = 'Schedule Time Off'
    def __init__(self, cmd: Commands.ScheduleTimeOff.ScheduleTimeOff):
        super().__init__(cmd)
        self.cmd = cmd
    def render_class(self, ctx: WovenContext, data):
        return "ScheduleTimeOff"
    def render_genericCommand(self, ctx: WovenContext, data):
        startTime = tags.input(id='startTime', type='text', class_='IDateTime', placeholder='Start Time')
        endTime = tags.input(id='endTime', type='number', step='0.5', placeholder='End Time')
        submit = tags.input(type='button', value='Schedule Vacation')[tags.Tag('athena:handler')(event='onclick', handler='scheduleVacation')]
        return self.preprocess([startTime, endTime, submit])
    @expose
    @Transaction
    def scheduleTimeOff(self, startTime, endTime):
        self.cmd.execute(self.employee, IDateTime(startTime), IDateTime(endTime))


registerAdapter(ScheduleTimeOff, Commands.ScheduleTimeOff.ScheduleTimeOff, IAthenaRenderable)
