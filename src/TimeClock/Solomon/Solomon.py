import warnings, datetime
from contextlib import contextmanager

from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.Utils import coerce, overload
try:
    import pymssql
    from pymssql import connect
except ImportError:
    warnings.warn("pymssql unavailable, Solomon database access unavailable")
    def connect(*a):
        raise RuntimeError("pymssql unavailable")
    pymssql = None

import os

user = os.environ.get('SOLOMONUSER')
host = os.environ.get('SOLOMONHOST')
db = os.environ.get('SOLOMONDATABASE')
pw = os.environ.get('SOLOMONPW')

if not user:
    warnings.warn("Solomon environment variables undefined, Solomon database access unavailable")
    pymssql = None


def fetchone(cur):
    r = cur.fetchone()
    if not r:
        return
    r = {i: r[i].strip() if isinstance(r[i], str) else r[i] for i in r}
    return r


def fetchall(cur):
    for r in cur:
        yield {i: r[i].strip() if isinstance(r[i], str) else r[i] for i in r}


@contextmanager
def context():
    with connect(host, user=user, database=db, password=pw) as con:
        with con.cursor(as_dict=True) as cur:
            yield cur


@coerce
def getEmployee(eid: str) -> dict:
    if not pymssql or eid == '1':
        return dummyEntry
    with context() as cur:
        cur.execute("SELECT * FROM employee WHERE EmpId=%s", (eid,))
        return fetchone(cur)


def getEmployees() -> [dict]:
    if not pymssql:
        yield dummyEntry
        return
    else:
        with context() as cur:
            cur.execute("SELECT * FROM employee")
            for i in fetchall(cur):
                yield i


def getSubAccounts() -> [dict]:
    with context() as cur:
        cur.execute("SELECT * FROM subacct")
        for i in fetchall(cur):
            yield i


@overload
def getSubAccount(eid: int) -> dict:
    if not pymssql:
        return {"Descr": "Dummy", "dfltExpSub": 1}
    with context() as cur:
        cur.execute("SELECT * FROM subacct WHERE Sub=%s", (eid,))
        return fetchone(cur)


@overload
def getSubAccount(eid: str) -> dict:
    if not pymssql:
        return {"Descr": "Dummy", "dfltExpSub": 1}
    with context() as cur:
        cur.execute("SELECT * FROM subacct WHERE Descr=%s", (eid,))
        return fetchone(cur)


def getWorkLocations() -> [dict]:
    with context() as cur:
        cur.execute("SELECT * FROM workloc")
        for i in fetchall(cur):
            yield i

def getWorkLocation(dfltWrkloc: str) -> dict:
    if not pymssql:
        return {"Descr": "Dummy", "dfltExpSub": 1}
    with context() as cur:
        cur.execute("SELECT * FROM workloc WHERE WrkLocId=%s", (dfltWrkloc,))
        return fetchone(cur)


@overload
def getBenefits(eid: str) -> [dict]:
    with context() as cur:
        cur.execute("SELECT * FROM benemp WHERE EmpID=%s", (eid,))
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
        cur.execute("SELECT * FROM benemp WHERE EmpID=%s and BenId=%s", (eid, bid))
        return fetchone(cur)


@overload
def getBenefit(bid: str) -> dict:
    with context() as cur:
        cur.execute("SELECT * FROM benefit WHERE BenId=%s", (bid,))
        return fetchone(cur)


@overload
def getBenefitAvailable(eid: str, bid: str) -> float:
    z = getBenefit(eid, bid)
    return z['CurrBYTDAvail'] + z['BYBegBal'] - z['BYTDUsed']


@overload
def getBenefitAvailable(eid: IEmployee, bid: str) -> float:
    return getBenefitAvailable(eid.employee_id, bid)


dummyEntry = {'DfltWrkloc': 'BRD   ',
              'StrtDate': datetime.datetime(2016, 6, 25, 0, 0),
              'Phone': '5555555555                    ',
              'Zip': '99206     ',
              'BirthDate': datetime.datetime(2017, 11, 2, 0, 0),
              'DfltExpSub': '011500                  ',
              'CalYr': '2016',
              'Addr2': '                                                            ',
              'Department': 'xxxxxx    ',
              'Status': 'I',
              'CpnyID': 'UGM       ',
              'EmpId': '1      ',
              'Name': 'John D. Doe Administrator                                           ',
              'Addr1': 'XXXXX E. XXXXXX Ave.                                       ',
              'SSN': '123456789',
              'City': 'Spokane                       ',
              'State': 'WA'
              }

