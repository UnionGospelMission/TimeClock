from collections import OrderedDict

from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Administrator import Administrator
from TimeClock.Database.Commands.ChangeAuthentication import ChangeAuthentication
from TimeClock.Database.Supervisor import Supervisor
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IDatabase.IEmployee import IEmployee
from TimeClock.ITimeClock.IDatabase.IPerson import IPerson
from TimeClock.ITimeClock.IDatabase.ISupervisee import ISupervisee
from TimeClock.ITimeClock.IDatabase.ISupervisor import ISupervisor
from TimeClock.ITimeClock.ISolomonEmployee import ISolomonEmployee
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Util import NULL
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderer.ConfirmationRenderer import ConfirmationRenderer
from TimeClock.Web.AthenaRenderer.ListRenderer import ListRenderer
from TimeClock.Web.Utils import formatShortName
from nevow import inevow
from nevow.athena import expose
from nevow.loaders import xmlfile
from nevow import tags as T


def formatPhone(n):
    if not n:
        return n
    if isinstance(n, str):
        if not n.isdigit():
            return n
        n = int(n)
    return ('(%i) %i-%i' % (n // 10000000, n // 10000 % 1000, n % 10000))

employee_attributes = OrderedDict()
employee_attributes['Name'] = "Name", None
employee_attributes['employee_id'] = "Employee ID", None
employee_attributes['active_directory_name'] = "Username", None
employee_attributes['emergency_contact_name'] = "Emergency Contact", None
employee_attributes['emergency_contact_phone'] = "Emergency Contact Phone", None
employee_attributes['Phone'] = "Phone", formatPhone
employee_attributes['Addr1'] = "Address 1", None
employee_attributes['Addr2'] = "Address 2", None
employee_attributes['City'] = "City", None
employee_attributes['State'] = "State", None
employee_attributes['Zip'] = "Zip", None
employee_attributes['StrtDate'] = "Start Date", lambda d: str(d.date())
employee_attributes['BirthDate'] = "Birth Date", lambda d: str(d.date())


@implementer(IAthenaRenderable)
class EmployeeRenderer(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/Employee.xml", "EmployeePattern")
    jsClass = "TimeClock.EmployeeRenderer"
    def __init__(self, person: IPerson):
        self._employee = IEmployee(person)
        print(50, self._employee, self.employee)
        self.solomonEmployee = ISolomonEmployee(self._employee)
        self.options = []
        self.commands = None
        self.selectedElement = None
        self.elements = {}
    def data_employeeData(self, ctx, data):
        d = self.solomonEmployee.record.copy()
        d.update(self._employee.persistentValues())
        return d
    def render_employeeDetails(self, ctx, data):
        row = inevow.IQ(ctx).patternGenerator('employeeDataPattern')
        o = []
        for k, e in employee_attributes.items():
            i, c = e
            if not c:
                def c(x):
                    return x
            o.append(row(data=dict(rowName=i, rowValue=c(data[-1][k]))))
        return o
    def render_employeeActions(self, ctx, data):
        if ISupervisor(self.employee, None) and self._employee in ISupervisor(self.employee).getEmployees():
            pass
        elif IAdministrator(self.employee, None):
            pass
        else:
            return ""
        self.commands = o = []
        api = self._employee.getAPI().api
        for c in api.getCommands(self._employee):
            iar = IAthenaRenderable(c, None)
            if iar:
                iar.prepare(self)
                iar.employee = self._employee
                self.elements[formatShortName(c.name)] = iar
                o.append({'name': c.name, 'value': iar})
        l = ListRenderer(o)
        l.prepare(self, self.showCommand, "Commands")
        l.visible = True
        l.selectable = False
        return l
    def showCommand(self, idx):
        c = self.commands[int(idx)]['value']
        if c.visible:
            c.hide()
        else:
            c.show()
    def render_employeeOptions(self, ctx, data):
        for k, i in self._employee.persistentValues().items():
            if k.startswith('emergency'):
                edit = T.input(name=k, value=i or "")
                self.options.append({'name': k, 'value': edit})
        if self.employee.isAdministrator():
            isSup = T.input(type='checkbox', name='isSupervisor')
            if ISupervisor(self._employee, None):
                isSup(checked='')
            isAdm = T.input(type='checkbox', name='isAdministrator')
            if IAdministrator(self._employee, None):
                isAdm(checked='')
            self.options.append({'name': 'username', 'value': T.input(name="active_directory_name", value=self._employee.active_directory_name or "")})
            self.options.append({'name': 'Is Supervisor', 'value': isSup})
            self.options.append({'name': 'Is Administrator', "value": isAdm})
            pbt = T.input(type='checkbox', name='payByTask')
            if self._employee.hourly_by_task:
                pbt(checked='')
            self.options.append({'name': 'Pay by Task', "value": pbt})
        save = T.input(type='button', value='Save Changes')[
            T.Tag("athena:handler")(event='onclick', handler='saveClicked')
        ]

        l = ListRenderer(self.options)
        l.selectable = False
        l.prepare(self, None, "Edit Employee")
        l.visible = True
        ret = [
            T.tr()[
                T.td()[
                    T.form(id='editEmployee')[
                        l]
                ]
            ],
            T.tr()[
                T.td()[
                    save
                ]
            ]
        ]
        for p in self.preprocessors:
            print(86, p)
            ret = p(ret)
        return ret
    @expose
    def saveClicked(self, args):
        return self.doSaveClicked(args, False)
    def doSaveClicked(self, args, force):
        kargs = dict(
            isAdministrator=False,
            isSupervisor=False,
            payByTask = False
        )

        for a in args:
            k = a['name']
            v = a['value']
            kargs[k] = v
        for k, v in kargs.items():
            # @TODO: Move into special commands
            if k.startswith('emergency'):
                setattr(self._employee, k, v)
            elif IAdministrator(self.employee):
                if k == 'payByTask':
                    if v == 'on':
                        self._employee.hourly_by_task = True
                    else:
                        self._employee.hourly_by_task = False
                elif k == 'isAdministrator':
                    print(132, v)
                    if v == 'on':
                        a = IAdministrator(self._employee, None)
                        if not a:
                            a = list(Store.query(Administrator, Administrator.employee == a))
                            if a:
                                a = a[0]
                            else:
                                a = IAdministrator(NULL)
                            a.employee = self._employee
                            self._employee.powerUp(a, IAdministrator)
                            a.powerUp(self._employee, IEmployee)
                    else:
                        a = IAdministrator(self._employee, None)
                        if a:
                            self._employee.powerDown(a, IAdministrator)
                elif k == 'isSupervisor':
                    if v == 'on':
                        a = ISupervisor(self._employee, None)
                        if not a:
                            a = list(Store.query(Supervisor, Supervisor.employee == a))
                            if a:
                                a = a[0]
                            else:
                                a = ISupervisor(NULL)
                            a.employee = self._employee
                            self._employee.powerUp(a, ISupervisor)
                            a.powerUp(self._employee, IEmployee)
                    else:
                        a = ISupervisor(self._employee, None)
                        if a:
                            employees = a.getEmployees()
                            if employees:
                                if force:
                                    for emp in employees:
                                        emp.supervisor = None
                                        a.powerDown(emp, ISupervisee)
                                else:
                                    cr = ConfirmationRenderer(self.doSaveClicked, args, True)
                                    cr.setMessage("This employee is a supervisor for the following employees. Please confirm you wish to proceed.")
                                    lr = ListRenderer([{"Employee ID": emp.employee_id, "Name": (ISolomonEmployee(emp).name)} for emp in employees])
                                    lr.visible = True
                                    lr.prepare(self, None, "Employees")
                                    cr.setData(lr)
                                    cr.prepare(self)
                                    return cr

                            self._employee.powerDown(a, ISupervisor)
                else:
                    setattr(self._employee, k, v)
        return False


registerAdapter(EmployeeRenderer, IPerson, IAthenaRenderable)
