from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce, overload
import os
try:
    from ldap3 import Server, Connection, NTLM
except ImportError:
    Server, Connection, NTLM = None

SERVER = os.environ.get('LDAPHOST').split(',')
DOMAIN = os.environ.get('LDAPDOMAIN', '')
USER_TEMPLATE = DOMAIN + r"\%s"


def getServer():
    if not Server:
        return None
    if not SERVER or not SERVER[0]:
        return None
    for s in SERVER:
        server = Server(s, connect_timeout=1, use_ssl=True)
        if server.check_availability():
            try:
                with Connection(server):
                    return server
            except:
                continue
    for s in SERVER:
        server = Server(s, connect_timeout=1)
        if server.check_availability():
            return server
    return None


def getConnection(server, username: str, pw: str):
    if not server:
        return None
    return Connection(server, user=USER_TEMPLATE % username, password=pw, authentication=NTLM, receive_timeout=10)


def runWithConnection(function, username, pw: str, args=()):
    conn = getConnection(getServer(), username, pw)
    if not conn:
        return False
    with conn:
        return function(conn, *args)


@overload
def authenticate(employee: IEmployee, pw: str):
    return runWithConnection(lambda conn: conn.bind(), employee.active_directory_name, pw)


@overload
def authenticate(employee_id: str, pw: str):
    return runWithConnection(lambda conn: conn.bind(), employee_id, pw)
