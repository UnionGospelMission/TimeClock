from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.File import File
from TimeClock.Database.LogEntry import LogEntry
from TimeClock.ITimeClock.IDatabase.ILogEntry import ILogEntry
from TimeClock.ITimeClock.IDatabase.ILogger import ILogger
from TimeClock.ITimeClock.IEvent.IEvent import IEvent
from TimeClock.ITimeClock.IEvent.IEventHandler import IEventHandler
from TimeClock.Util.DateTime import DateTime
from TimeClock.Utils import coerce
from axiom.item import Item

from axiom.attributes import text, integer, reference


INFO = 0x1
DEBUG = 0x2
WARN = 0x4
ERROR = 0x8


@implementer(ILogger, IEventHandler)
class Logger(Item):
    name = text()
    flags = integer()
    file = reference()
    @coerce
    def log(self, level: int, message: str):
        if level & self.flags and self.file:
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

    def handleEvent(self, event: IEvent):
        self.info(event)


def findOrCreateLogger(lid: str):
    from TimeClock.Axiom.Store import Store
    logger = list(Store.query(Logger, Logger.name==lid))
    if logger:
        return logger[0]
    logger = Logger(store=Store, name=lid, flags=INFO + DEBUG + WARN + ERROR)
    if Store.filesdir:
        logger.file = File(store=Store, path=Store.filesdir.child('%s.log' % lid).path)
    return logger


registerAdapter(findOrCreateLogger, str, ILogger)
