from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IDatabaseEvent import IDatabaseEvent
from TimeClock.ITimeClock.IEvent.IEvent import IEvent


class ICommandEvent(IEvent):
    def getCaller() -> IEmployee:
        pass

    def getCommand() -> ICommand:
        pass

    def getArgs() -> [object]:
        pass
