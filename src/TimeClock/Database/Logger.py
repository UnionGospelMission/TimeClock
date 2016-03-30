from zope.interface import implementer

from TimeClock.Database.LogEntry import LogEntry
from TimeClock.ITimeClock.IDatabase.ILogEntry import ILogEntry
from TimeClock.ITimeClock.IDatabase.ILogger import ILogger
from TimeClock.ITimeClock.IEvent.IAbstractEvent import IAbstractEvent
from TimeClock.Util.DateTime import DateTime
from TimeClock.Utils import coerce
from axiom.item import Item

from axiom.attributes import text, integer, reference


INFO = 0x1
DEBUG = 0x2
WARN = 0x4
ERROR = 0x8


@implementer(ILogger)
class Logger(Item):
    name = text()
    flags = integer()
    file = reference()
    @coerce
    def log(self, level: int, message: str):
        if level & self.flags:
            with self.file.open('a') as f:
                print(str(DateTime.now()), message, file=self.file, flush=True)
        self.powerUp(LogEntry(store=self.store, level=level, message=message, logger=self), ILogEntry)
    def warn(self, message: str):
        self.log(WARN, message)

    def info(self, message: str):
        self.log(INFO, message)

    def debug(self, message: str):
        self.log(DEBUG, message)

    def error(self, message: str):
        self.log(ERROR, message)

    def handleEvent(self, event: IAbstractEvent):
        self.info(event)

