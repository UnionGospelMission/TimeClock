from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce, overload


def runWithConnection(function, username, pw: str, args=()):
    from ldap3 import Server, Connection, ALL, NTLM
    server = Server('192.168.0.10', connect_timeout=10)
    with Connection(server, user=r"UGM\%s" % username, password=pw, authentication=NTLM, receive_timeout=10) as conn:
        return function(conn, *args)


@overload
def authenticate(employee: IEmployee, pw: str):
    return runWithConnection(lambda conn: conn.bind(), employee.active_directory_name, pw)


@overload
def authenticate(employee_id: str, pw: str):
    return runWithConnection(lambda conn: conn.bind(), employee_id, pw)
