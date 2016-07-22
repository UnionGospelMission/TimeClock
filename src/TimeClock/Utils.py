import re
import arrow
import time

from TimeClock.ITimeClock.IDateTime import IDateTime
from .Util.Coerce import Coercer
from .Util.Overload import Overloader
from .Util import fromFunction
from .Util.subclass import issubclass, Subclass

def coerce(func):
    return Coercer(func)


def overload(func):
    return Overloader().add(func)


@coerce
def getAllEmployees() -> list:
    from TimeClock.Axiom.Store import Store
    from TimeClock.Database.Employee import Employee
    return Store.query(Employee)

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
    HAST=-600
)



tzpattern = re.compile('([A-Z0-9a-z]{3,4})$')


def getIDateTime(strtime) -> IDateTime:
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
        val = IDateTime(strtime.strip() + default_tzoffsetstr)
    return val
