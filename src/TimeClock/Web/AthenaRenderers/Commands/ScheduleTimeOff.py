from TimeClock import Exceptions
from TimeClock.Utils import coerce
from twisted.python.components import registerAdapter

from TimeClock.Axiom import Transaction
from TimeClock.Database import Commands
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.Events.TimeEntryCreatedEvent import TimeEntryCreatedEvent
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile
from TimeClock.ITimeClock.IDatabase.IEntryType import IEntryType


class ScheduleTimeOff(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.ScheduleTimeOff'
    subaccounts = None
    name = 'Schedule Time Off'

    def __init__(self, cmd: Commands.ScheduleTimeOff.ScheduleTimeOff):
        super().__init__(cmd)
        self.cmd = cmd

    def render_class(self, ctx: WovenContext, data):
        return "ScheduleTimeOff"

    def getSubs(self, se):
        subs = []
        for a in self.employee.getSubAccounts():
            o = tags.option(value=a.sub)[a.name]
            if se.defaultSubAccount == a:
                o(selected='')
                return [o]
            subs.append(o)
        return subs

    def getWLocs(self, se):
        locs = []
        for b in self.employee.getWorkLocations():
            o = tags.option(value=b.workLocationID)[b.description]
            if se.defaultWorkLocation == b:
                o(selected='')
                return [o]
            locs.append(o)
        return locs

    def render_genericCommand(self, ctx: WovenContext, data):
        startTime = tags.input(id='startTime', type='text', class_='IDateTime', placeholder='Start Time')
        endTime = tags.input(id='hours', type='number', step='0.5', placeholder='Hours')

        se = ISolomonEmployee(self.employee)
        s = tags.select(id="sub", style='display:none')[self.getSubs(se)]

        w = tags.select(id='wloc', style='display:none')[self.getWLocs(se)]
        typ = tags.select(id='type')[
            tags.option(value='Vacation')['Vacation'],
            tags.option(value='Illness')['Sick Leave'],
            #tags.option(value='Personal')['Personal']
        ]
        submit = tags.input(type='button', value='Schedule Time Off')[tags.Tag('athena:handler')(event='onclick', handler='scheduleTimeOff')]
        return self.preprocess([startTime, endTime, s, w, typ, submit])

    @expose
    @Transaction
    def scheduleTimeOff(self, startTime: str, duration: float, typ: IEntryType, sub: ISubAccount, wloc: IWorkLocation):
        duration = float(duration)
        if duration > 10:
            self.callRemote("alert", '<div>Please submit a separate time off request for each day you plan to be gone.</div>')
            return False
        else:
            startTime = startTime + ' 00:00:00 AUTO'
            entry = self.cmd.execute(self.employee, self.employee, IDateTime(startTime), float(duration), IEntryType(typ), ISubAccount(sub), IWorkLocation(wloc))
            c = TimeEntryCreatedEvent(entry)
            IEventBus("Web").postEvent(c)
        return True



registerAdapter(ScheduleTimeOff, Commands.ScheduleTimeOff.ScheduleTimeOff, IAthenaRenderable)
