from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IEvent.IAbstractEvent import IAbstractEvent


class ICommandEvent(IAbstractEvent):
    def getCaller() -> IEmployee:
        pass

    def getCommand() -> ICommand:
        pass

    def getArgs() -> [object]:
        pass
