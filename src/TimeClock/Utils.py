import re
import arrow
import time

from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.Util.I_Coerce import I_Coercer
from .Util.Coerce import Coercer
from .Util.Overload import Overloader
from .Util import fromFunction
from .Util.subclass import issubclass, Subclass


def coerce(func):
    return Coercer(func)


def i_coerce(func):
    return I_Coercer(func)


def overload(func):
    return Overloader().add(func)


@coerce
def getAllEmployees() -> list:
    from TimeClock.Axiom.Store import Store
    from TimeClock.Database.Employee import Employee
    return Store.query(Employee)


@coerce
def getAllSubAccounts() -> list:
    from TimeClock.Axiom.Store import Store
    from TimeClock.Database.SubAccount import SubAccount
    return Store.query(SubAccount)


@coerce
def getAllWorkLocations() -> list:
    from TimeClock.Axiom.Store import Store
    from TimeClock.Database.WorkLocation import WorkLocation
    return Store.query(WorkLocation)

TZOffsets = dict(
    PST=-480,
    PDT=-420,
    CDT=-300,
    CST=-360,
    EDT=-240,
    EST=-300,
    MDT=-360,
    MST=-420,
    AKDT=-480,
    AKST=-540,
    HADT=-540,
    HAST=-600,
    UTC=0
)


tzpattern = re.compile('([A-Z0-9a-z]{3,4})$')
hmtzpattern = re.compile('....-..-.. [0-9]{1,2}:[0-9]{2}:[0-9]{2} ([-0-9]{1,2}:[0-9]{2})')
datetimepattern = re.compile('^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}) (?P<hour>[0-9]{2}):(?P<min>[0-9]{2}):(?P<second>[0-9]{2})(?: (?P<zone>[A-Z0-9a-z]{3,4}))?$')


def getIDateTime(strtime) -> IDateTime:
    dt = datetimepattern.search(strtime)
    val = None
    if dt:
        groups = {i: (int(v) if (v and v.isdigit()) else v) for i, v in dt.groupdict().items()}
        if groups['zone'] is None or groups['zone'] == 'AUTO':
            val = IDateTime(0).replace(year=groups['year'], month=groups['month'], day=groups['day'], hour=groups['hour'], minute=groups['min'], second=groups['second'])
    if val is None:
        default_tzoffset = (arrow.get(time.localtime()) - arrow.get(time.gmtime())).total_seconds() / 60
        if default_tzoffset > 0:
            default_tzoffsetstr = '%02i:%02i' % (int(default_tzoffset / 60), int(default_tzoffset) % 60)
        else:
            default_tzoffsetstr = '%03i:%02i' % (int(default_tzoffset / 60), int(default_tzoffset) % 60)
        tz = tzpattern.search(strtime)
        if tz:
            tz = tz.group(0)
            if tz == 'AUTO':
                val = IDateTime(strtime.replace(tz, '').strip() + default_tzoffsetstr)
                return val
            tzoffset = TZOffsets[tz]
            if tzoffset > 0:
                tzoffsetstr = '%02i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
            else:
                tzoffsetstr = '%03i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
            val = IDateTime(strtime.replace(tz, '').strip() + tzoffsetstr)
        else:
            tz = hmtzpattern.search(strtime)
            if tz:
                tz = tz.group(1)
                hrs, mins = tz.split(':')
                tzoffset = int(hrs) * 60 + int(mins)
                if tzoffset > 0:
                    tzoffsetstr = '%02i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                else:
                    tzoffsetstr = '%03i:%02i' % (int(tzoffset / 60), int(tzoffset) % 60)
                val = IDateTime(strtime.strip() + tzoffsetstr)
            else:
                val = IDateTime(strtime.strip() + default_tzoffsetstr)
    return val
