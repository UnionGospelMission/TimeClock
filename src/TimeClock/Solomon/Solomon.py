from contextlib import contextmanager
from TimeClock.Utils import coerce, overload
from pymssql import connect
import os
user = os.environ['SOLOMONUSER']
host = os.environ['SOLOMONHOST']
db = os.environ['SOLOMONDATABASE']
pw = os.environ['SOLOMONPW']


@contextmanager
def context():
    with connect(host, user=user, database=db, password=pw) as con:
        with con.cursor(as_dict = True) as cur:
            yield cur


@coerce
def getEmployee(eid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM employee WHERE EmpId='%s'"%eid)
        return cur.fetchone()


@coerce
def getArea(eid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM subacct WHERE Sub='%s'"%eid)
        return cur.fetchone()


def getWorkLocation(dfltWrkloc: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM workloc WHERE WrkLocId='%s'" % dfltWrkloc)
        return cur.fetchone()
