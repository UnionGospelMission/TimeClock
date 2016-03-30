from TimeClock.Axiom.Attributes import datetime
from TimeClock.Util.DateTime import DateTime
from axiom.attributes import reference

from axiom.attributes import integer, text
from zope.interface import implementer

from axiom.item import Item

from TimeClock.ITimeClock.IDatabase.ILogEntry import ILogEntry


@implementer(ILogEntry)
class LogEntry(Item):
    level = integer()
    message = text()
    logger = reference()
    timestamp = datetime(defaultFactory=lambda *x: DateTime.now())
