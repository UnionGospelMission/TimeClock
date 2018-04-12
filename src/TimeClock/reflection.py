from datetime import datetime

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.File import File
from TimeClock.Database.Logger import Logger
from TimeClock.Database.StaticAuthenticationMethod import StaticAuthenticationMethod
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IEvent.IDatabaseEvent.ICommandEvent import ICommandEvent
from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus

from TimeClock.Util import NULL
from nevow import inevow
from nevow.flat import registerFlattener
from .API import APIs
from .Database import Reflection
from .Event import EventBus
import TimeClock.API.Permissions
import TimeClock.Web.AthenaRenderers
from .Database import SubAccount, Supervisor, Administrator
from .Database.TimeEntry import TimeEntry
from .Database.WorkLocation import WorkLocation
from .Database.EntryType import EntryType
from .Database.TimePeriod import TimePeriod
from .API import CalendarData
from .Solomon import SolomonEmployee
from .Solomon import Solomon
from .Database.Permissions import Permission
from .ITimeClock.IDateTime import IDateTime
from nevow.inevow import IRendererFactory

@implementer(inevow.IRenderer)
class FlattenDate(object):
    def __init__(self, dt):
        self.dt = dt
    def rend(self, ctx):
        return str(self.dt)

registerAdapter(FlattenDate, datetime, inevow.IRenderer)

registerFlattener(lambda x, y: str(x), datetime)


from nevow import athena
mangleID_ = athena._mangleId


def mangleId(oldId):
    if 'athenaid:' in str(oldId) or 'athena:' in str(oldId):
        return oldId
    return mangleID_(oldId)

athena._mangleId = mangleId


import TimeClock.API.EventBus
import TimeClock.Util.TimeEntryValidator
from TimeClock.Report.Format import Widget

from TimeClock.Database.CacheAuthenticationMethod import CacheAuthenticationMethod

from TimeClock.Database.Benefit import Benefit

import os
if os.environ.get('DEBUG_STACK'):
    import stack_tracer
    stack_tracer.trace_start('/home/timeclock/stack.html')

    from TimeClock.Util.DateTime import DateTime
    from TimeClock.ITimeClock.IEvent.IEvent import IEvent
    from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler


    @implementer(IEventHandler)
    class Logger(object):
        f = open('/tmp/webevent.log', 'a')

        def handleEvent(self, event: IEvent):
            print(str(DateTime.now()), event, vars(event), file=self.f, flush=True)
            print(str(DateTime.now()), event)

        def powerUp(self, *a):
            pass

    IEventBus("Web").register(Logger(), IEvent)
