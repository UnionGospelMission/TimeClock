import dis

import time

import io

import datetime

from TimeClock.API.CalendarData import CalendarData
from TimeClock.Database.Employee import Employee
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.Database.WorkLocation import WorkLocation
from TimeClock.ITimeClock.IDatabase.ICalendarData import ICalendarData
from TimeClock.ITimeClock.IDatabase.ITimeEntry import ITimeEntry
from TimeClock.ITimeClock.IDatabase.IWorkLocation import IWorkLocation
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from TimeClock.Sandbox.Sandbox import Sandbox
from TimeClock.Sandbox.Function import Function
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Axiom import Store
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Util.DateTime import DateTime
from TimeClock.Utils import overload
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReport import IReport
from nevow import tags


@implementer(IReport)
class DynamicReport(Item):
    name = text()
    code = text()
    description = text()

    def __setattr__(self, key, value):
        if key == 'code':
            if Function in self._inMemoryPowerups:
                self._inMemoryPowerups.pop(Function)
        super().__setattr__(key, value)

    def prepare(self):
        f = list(self.powerupsFor(Function))
        if f:
            return f[0]
        code = compile(self.code, self.name, "exec")

        if code.co_code[0] == dis.opmap['LOAD_CONST']:
            c = code.co_code[1] + code.co_code[2] * 256
            arguments = code.co_consts[c]
            if not isinstance(arguments, tuple):
                arguments = ()
            for arg in arguments:
                if isinstance(arg, tuple) and len(arg) == 2:
                    continue
                if not isinstance(arg, str):
                    arguments = ()
                    break
        else:
            arguments = ()
        function = Function(self.name, code, arguments, None)
        self.inMemoryPowerUp(function, Function)
        return function

    @overload
    def runReport(self, FormatFactory: IFormatterFactory, parameters: [object]):
        formatter = IFormat(FormatFactory())
        return self.runReport(formatter, parameters)
    @overload
    def runReport(self, formatter: IFormat, parameters: [object]):
        function = self.prepare()
        debug = io.StringIO()
        # dis.dis(compile(self.code, self.name, "exec"), file=debug)
        globs = dict(
            formatter=formatter,
            formatHeader=formatter.formatHeader,
            formatFooter=formatter.formatFooter,
            formatRow=formatter.formatRow,
            parameters=parameters,
            arguments=parameters,
            print=print,
            IDateTime=IDateTime,
            ISubAccount=ISubAccount,
            IEmployee=IEmployee,
            ISolomonEmployee=ISolomonEmployee,
            ICalendarData=ICalendarData,
            allEmployees=lambda: list(Store.Store.query(Employee)),
            allSubAccounts=lambda: (i for i in Store.Store.query(SubAccount) if i.active),
            allWorkLocations=lambda: (i for i in Store.Store.query(WorkLocation) if i.active),
            int=int,
            float=float,
            str=str,
            tuple=tuple,
            list=list,
            today=DateTime.today,
            tr=tags.tr,
            td=tags.td,
            tbody=tags.tbody,
            now=time.time
        )
        functions = list(globs.values()) + formatter.functions
        functions.append(DateTime.strftime)
        functions.extend([
            CalendarData.sumBetween,
            CalendarData.between,
            CalendarData.addTime,
            Employee.getEntries,
            datetime.timedelta.total_seconds,
            SubAccount.getEmployees,
            Employee.getWorkLocations,
            WorkLocation.getEmployees,
            Employee.getWorkLocations,
            Employee.viewHours
        ])
        exc = Sandbox(None, function,
                      parameters,
                      globals_=globs,
                      functions=functions,
                      attributes_accessible=(Item, IEmployee, ISolomonEmployee, ISubAccount, IDateTime, formatter, ICalendarData, ITimeEntry, IWorkLocation, datetime.timedelta),
                      )
        g = exc.execute(10000, 10)
        n = next(g)
        while True:
            if n == Sandbox.SUSPEND_TIME:
                n = g.send(10)
            elif n == Sandbox.SUSPEND_INST:
                n = g.send(10000)
            else:
                break
            if exc.counter > 1000000:
                raise TimeoutError("Report has exceeded 1,000,000 instructions")
        return formatter.getReport()

    def getDescription(self) -> str:
        return self.description

    def getArgs(self) -> [str]:
        function = self.prepare()
        return function.arguments
