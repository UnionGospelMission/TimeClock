from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IItem import IItem


class IAuthenticationMethod(IItem):
    def authenticate(employee: IEmployee, password: bytes) -> bool:
        pass
