from zope.interface import implementer

from TimeClock.Event.AbstractEvent import AbstractEvent
from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IEvent.IDatabaseEvent.ICommandEvent import ICommandEvent
from TimeClock.Utils import coerce


@implementer(ICommandEvent)
class CommandEvent(AbstractEvent):
    cancellable = True
    cancelled = False
    retval = None
    finished = False

    @coerce
    def __init__(self, caller: IPerson, command: ICommand, *args):
        self.caller = caller
        self.command = command
        self.args = args
    def getCaller(self) -> IEmployee:
        return self.caller

    def getCommand(self) -> ICommand:
        return self.command

    def getArgs(self) -> [object]:
        return self.args

    def getType(self) -> ICommandEvent:
        return ICommandEvent

    def __repr__(self):
        return "<CommandEvent %s %r %s>" % (self.command.name, self.caller, str(self.args))

    def cancel(self) -> bool:
        assert self.cancellable
        self.cancelled = True
        return self.cancelled

    def setReturn(self, retval: object) -> bool:
        self.retval = retval
        return True

    def setFinished(self, finished: bool) -> bool:
        self.finished = True
        return True

    def getFinished(self) -> bool:
        return self.finished
