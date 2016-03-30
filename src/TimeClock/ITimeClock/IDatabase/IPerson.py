from TimeClock.ITimeClock.IDatabase.IItem import IItem
from TimeClock.ITimeClock.IDatabase.IPermission import IPermission


class IPerson(IItem):
    def getPermissions() -> [IPermission]:
        pass
