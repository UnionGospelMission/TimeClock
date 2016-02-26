from contextlib import contextmanager

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce, overload
from pymssql import connect
import os
user = os.environ['SOLOMONUSER']
host = os.environ['SOLOMONHOST']
db = os.environ['SOLOMONDATABASE']
pw = os.environ['SOLOMONPW']


def fetchone(cur):
    r = cur.fetchone()
    if isinstance(r, str):
        return r.strip()
    return r


def fetchall(cur):
    o = []
    for i in cur:
        if isinstance(i, str):
            o.append(i.strip())
        else:
            o.append(i)
    return o


@contextmanager
def context():
    with connect(host, user=user, database=db, password=pw) as con:
        with con.cursor(as_dict = True) as cur:
            yield cur


@coerce
def getEmployee(eid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM employee WHERE EmpId='%s'"%eid)
        return fetchone(cur)


@coerce
def getArea(eid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM subacct WHERE Sub='%s'"%eid)
        return fetchone(cur)


def getWorkLocation(dfltWrkloc: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM workloc WHERE WrkLocId='%s'" % dfltWrkloc)
        return fetchone(cur)


@overload
def getBenefits(eid: str) -> [dict]:
    with context() as cur:
        cur.execute("SELECT * FROM benemp WHERE EmpID='%s'" % eid)
        return fetchall(cur)


@overload
def getBenefits(e: IEmployee) -> [dict]:
    return getBenefits(e.employee_id)


@overload
def getBenefit(e: IEmployee, bid: str) -> [dict]:
    return getBenefit(e.employee_id, bid)


@overload
def getBenefit(eid: str, bid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM benemp WHERE EmpID='%s' and BenId='%s'" % (eid, bid))
        return fetchone(cur)


@overload
def getBenefit(bid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM benefit WHERE BenId='%s'" % bid)
        return fetchone(cur)


@overload
def getBenefitAvailable(eid: str, bid: str) -> float:
    z = getBenefit(eid, bid)
    return z['CurrBYTDAvail'] + z['BYBegBal'] - z['BYTDUsed']


@overload
def getBenefitAvailable(eid: IEmployee, bid: str) -> float:
    return getBenefitAvailable(eid.employee_id, bid)


