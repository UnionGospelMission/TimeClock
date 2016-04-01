from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce


@coerce
def authenticate(employee: IEmployee, pw: str):
    from ldap3 import Server, Connection, ALL, NTLM
    server = Server('192.168.0.10')
    conn = Connection(server, user="UGM\\%s"%employee.active_directory_name, password=pw, authentication=NTLM)
    return conn.bind()
