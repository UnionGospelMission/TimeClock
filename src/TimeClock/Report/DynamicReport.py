import dis

from TimeClock.Database.Employee import Employee
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.Executor.Executor import Executor
from TimeClock.Executor.Function import Function
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.ISubAccount import ISubAccount
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Axiom import Store
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.Solomon.SolomonEmployee import SolomonEmployee
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReport import IReport


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
        dis.dis(code)
        if code.co_code[0] == dis.opmap['LOAD_CONST']:
            c = code.co_code[1] + code.co_code[2] * 256
            arguments = code.co_consts[c]
            if not isinstance(arguments, tuple):
                print(43)
                arguments = ()
            for arg in arguments:
                print(45, arg)
                if isinstance(arg, tuple) and len(arg) == 2:
                    print(47)
                    continue
                if not isinstance(arg, str):
                    print(50, arg)
                    arguments = ()
                    break
        else:
            arguments = ()
        function = Function(self.name, code, arguments, None)
        self.inMemoryPowerUp(function, Function)
        return function

    def runReport(self, Format: IFormat, parameters: [object]) -> bytes:
        formatter = Format()
        function = self.prepare()
        globs = dict(
            formatHeader=formatter.formatHeader,
            formatFooter=formatter.formatFooter,
            formatRow=formatter.formatRow,
            parameters=parameters,
            print=print,
            ISubAccount=ISubAccount,
            IEmployee=IEmployee,
            ISolomonEmployee=ISolomonEmployee,
            allEmployees=lambda: list(Store.Store.query(Employee)),
            allSubAccounts=lambda: list(Store.Store.query(SubAccount)),
            int=int,
            float=float,
            str=str,
        )

        exc = Executor(None, function,
                       parameters,
                       globals=globs,
                       functions=globs.values(),
                       attributes_accessible=(Item, Employee, SolomonEmployee, SubAccount),
                       )
        g = exc.execute(10000, 10)
        n = next(g)
        while n == Executor.SUSPEND:
            n = n.tell(1)
        return formatter.getReport()

    def getDescription(self) -> str:
        return self.description

    def getArgs(self) -> [str]:
        function = self.prepare()
        print(79, function.arguments)
        return function.arguments
