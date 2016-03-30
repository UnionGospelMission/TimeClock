from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce


@coerce
def authenticate(employee: IEmployee, pw: str):
    from ldap3 import Server, Connection, ALL, NTLM
    server = Server('ipa.demo1.freeipa.org')
    conn = Connection(server, user="Domain\\User", password=pw, authentication=NTLM)
    conn.extend.standard.who_am_i()

