from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer
from nevow.athena import expose


class AbstractCommandRenderer(AbstractRenderer):
    jsClass = "TimeClock.Commands"
    @expose
    def runCommand(self, args):
        a = self.processArgs(args)
        print(13, a)
        return self.execute(*a)
    def processArgs(self, args):
        print(15, args)
        a = []
        for i in args:
            a.append(i['value'])
        print(19, args)
        return a
    def execute(self, *a):
        emp = IAdministrator(self.employee, None) or ISupervisor(self.employee, None) or self.employee
        print(23, emp, a, self.employee)
        return self.command.execute(emp, *a)
    def __init__(self, command: ICommand):
        self.command = command
        self.name = command.name
    def render_actionName(self, ctx, idata):
        return self.command.name
