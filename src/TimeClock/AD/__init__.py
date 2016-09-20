from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce


def runWithConnection(function, username, pw: str, args=()):
    from ldap3 import Server, Connection, ALL, NTLM
    server = Server('192.168.0.10', connect_timeout=1)
    with Connection(server, user=r"UGM\%s" % username, password=pw, authentication=NTLM) as conn:
        return function(conn, *args)


@coerce
def authenticate(employee: IEmployee, pw: str):
    return runWithConnection(lambda conn: conn.bind(), employee.active_directory_name, pw)

