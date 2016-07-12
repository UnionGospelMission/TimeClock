import dis

from TimeClock.Database.Employee import Employee
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from TimeClock.Sandbox.Sandbox import Sandbox
from TimeClock.Sandbox.Function import Function
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Axiom import Store
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Solomon.SolomonEmployee import SolomonEmployee
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
        dis.dis(compile(self.code, self.name, "exec"))
        globs = dict(
            formatter=formatter,
            formatHeader=formatter.formatHeader,
            formatFooter=formatter.formatFooter,
            formatRow=formatter.formatRow,
            parameters=parameters,
            print=print,
            IDateTime=IDateTime,
            ISubAccount=ISubAccount,
            IEmployee=IEmployee,
            ISolomonEmployee=ISolomonEmployee,
            allEmployees=lambda: list(Store.Store.query(Employee)),
            allSubAccounts=lambda: list(Store.Store.query(SubAccount)),
            int=int,
            float=float,
            str=str,
            tuple=tuple,
            list=list,
            today=DateTime.today,
            tr=tags.tr,
            td=tags.td,
            tbody=tags.tbody
        )

        exc = Sandbox(None, function,
                      parameters,
                      globals_=globs,
                      functions=list(globs.values()) + formatter.functions,
                      attributes_accessible=(Item, Employee, SolomonEmployee, SubAccount, DateTime, formatter),
                      )
        g = exc.execute(10000, 10)
        n = next(g)
        while n == Sandbox.SUSPEND:
            n = n.tell(1)
        return formatter.getReport()

    def getDescription(self) -> str:
        return self.description

    def getArgs(self) -> [str]:
        function = self.prepare()
        return function.arguments
