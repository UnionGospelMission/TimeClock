import dis

import io


from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.IReport.IFormatterFactory import IFormatterFactory
from TimeClock.Report.Access.AFunction import AFunction
from TimeClock.Report.Access.AReport import AReport
from TimeClock.Report.Log import Log
from TimeClock.Sandbox.Sandbox import Sandbox
from TimeClock.Sandbox.Function import Function
from TimeClock.ITimeClock.IReport.IFormat import IFormat
from TimeClock.Utils import overload
from axiom.attributes import text

from axiom.item import Item
from zope.interface import implementer

from TimeClock.ITimeClock.IReport.IReport import IReport
from nevow import tags
from TimeClock.Report.IAccess import interfaces
from twisted.internet import reactor

sampleReport = """
# This is a sample report
# Arguments for the report are placed in a tuple at the top
(('From Date', 'IDateTime'), ('To Date', 'IDateTime'), ("Limit", "int"))

# The first entry in each 2-tuple is the name of the variable, the second entry is the type.
# Supported types are the python primitive types (str, int, float) and date-times (IDateTime)
# Spaces in the variable name are removed, and the first letter is lower-cased, so 'From Date'
# becomes the variable `fromDate`

# Reports are written in functional python3.5
# Class creation, assertions, and exceptions are unavailable, but new functions can be declared

def factorial(n):
    if n < 1:
        return 1
    return n * factorial(n - 1)

# The following names are declared in the global namespace
# Report: The top level object representing this report
# documentation for Report, and the other objects it references can be found at /Reports/

# int(n): converts the given argument to a python {int}
# float(n): converts the given argument to a python {float}
# str(n): converts the given argument to a python {str}
# tuple(n): converts the given argument to a python {tuple}
# list(n): converts the given argument to a python {list}
# n may be omitted, in which case a null default is used (0, '', [])


# IDateTime(n): creates a new IDateTime object, either seconds since EPOCH or a string in ISO format
# divmod(a, b): Return the tuple ((x - x % y) / y, x % y)
# len: returns the length of an iterable, if the iterable is a generator, it is consumed

# Output for the report is created using 2 functions
# The following creates a header row with 2 columns

Report.formatHeader(["Sample Header 1", "Sample Header 2"])

# Rows in the report are then added.  The columns must be initialized via `Report.formatHeader` before rows may be added
# All columns specified in `Report.formatHeader` must be included in the row, extra columns in the row are ignored
Report.formatRow({"Sample Header 1": factorial(1), "Sample Header 2": factorial(10)})

# If the report needs to adjust the output based on the format selected, the name of the format is available in
# Report.formatterName

Report.print("This report uses the", Report.formatterName, "format")

# If the report raises an exception, the disassembled code is logged to the calling client as a crude traceback.
# The function with the problem will be shown at the bottom, the stackPointer gives the bytecode index of the next
# instruction, the line number holding the instruction is given in the left column.

"""


@implementer(IReport)
class DynamicReport(Item):
    name = text()
    code = text(default=sampleReport)
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
    def runReport(self, FormatFactory: IFormatterFactory, parameters: [object], log: Log, callback):
        formatter = IFormat(FormatFactory())
        return self.runReport(formatter, parameters, log, callback)

    @overload
    def runReport(self, formatter: IFormat, parameters: [object], log: Log, callback):
        function = self.prepare()

        a_report = AReport(formatter, self.store, log, interfaces)
        globs = dict(
            Report=a_report,
            int=AFunction(int),
            float=AFunction(float),
            str=AFunction(str),
            tuple=AFunction(tuple),
            list=AFunction(list),
            tr=AFunction(tags.tr),
            td=AFunction(tags.td),
            tbody=AFunction(tags.tbody),
            IDateTime=AFunction(IDateTime),
            divmod=AFunction(divmod),
            len=AFunction(len),
            iter=AFunction(iter)
        )
        globs.update(
            {i.getName(): i
             for i in interfaces})

        DynamicReport.exc = exc = Sandbox(None, function,
                      parameters,
                      globals_=globs,
                      interfaces=a_report.getInterfaces()
                      )
        g = exc.execute(1, 0.1)
        n = next(g)

        def cont(ni):
            try:
                if ni == Sandbox.SUSPEND_TIME:
                    ni = g.send(0.1)
                elif ni == Sandbox.SUSPEND_INST:
                    ni = g.send(10000)
                else:
                    callback(formatter.getReport())
                    return

                if exc.counter > 1000000:
                    raise TimeoutError("Report has exceeded 1,000,000 instructions")
            except:
                import traceback
                a_report.log('ERROR', traceback.format_exc().replace('\n', '<br/>'))
                s_exc = exc
                while s_exc.sub:
                    a_report.log('ERROR', 'stackPointer: %i' % s_exc.index)
                    debug = io.StringIO()
                    dis.dis(s_exc.function.code, file=debug)
                    a_report.log('CODE<br/>', debug.getvalue().replace('\n', '<br/>'))
                    s_exc = s_exc.sub
                a_report.log('ERROR', 'stackPointer: %i' % s_exc.index)
                debug = io.StringIO()
                dis.dis(s_exc.function.code, file=debug)
                a_report.log('CODE<br/>', debug.getvalue().replace('\n', '<br/>'))
                raise
            reactor.callLater(0.0001, cont, ni)

        cont(n)

    def getDescription(self) -> str:
        return self.description

    def getArgs(self) -> [str]:
        function = self.prepare()
        return function.arguments
