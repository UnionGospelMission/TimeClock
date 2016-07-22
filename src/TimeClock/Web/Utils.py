import re

from TimeClock.Util.OrderedDict import OrderedDict


def formatShortName(n):
    n=n.title().replace(' ', '')
    return n[0].lower() + n[1:]


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
employee_attributes['Status'] = "Active", lambda a: a == 'A'
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

