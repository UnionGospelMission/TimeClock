from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission
from TimeClock.Utils import overload


class AbstractAPI(object):
    @overload
    def getCommands(self) -> [ICommand]:
        return self.powerupsFor(ICommand)
    @overload
    def getCommands(self, permissions: [IPermission]) -> [ICommand]:
        return [c for c in self.powerupsFor(ICommand) if c.hasPermission(permissions)]
    def __getitem__(self, value: str) -> ICommand:
        return next(c for c in self.powerupsFor(ICommand) if c.name == value)
    @overload
    def getCommandNames(self) -> [str]:
        return (c.name for c in self.powerupsFor(ICommand))
    @overload
    def getCommandNames(self, permissions: [IPermission]) -> [str]:
        return (c.name for c in self.powerupsFor(ICommand) if c.hasPermission(permissions))
    def __getattr__(self, item):
        if '_' in item:
            return super(AbstractAPI, self).__getattribute__(item)
        for i in self.getCommandNames():
            n = i.title().replace(' ', '')
            if item == n[0].lower() + n[1:]:
                return self[i].execute
        return super(AbstractAPI, self).__getattribute__(item)

