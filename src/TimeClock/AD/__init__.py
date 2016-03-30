from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce


@coerce
def authenticate(employee: IEmployee, pw: bytes) -> IEmployee:
    if employee.alternate_authentication:
        return employee.alternate_authentication
