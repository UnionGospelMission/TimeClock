from TimeClock.ITimeClock.IDateTime import IDateTime
from TimeClock.ITimeClock.ITimeDelta import ITimeDelta
from TimeClock.Report.IAccess.IABenefit import IABenefit
from TimeClock.Report.IAccess.IACalendarData import IACalendarData
from TimeClock.Report.IAccess.IAEmployee import IAEmployee
from TimeClock.Report.IAccess.IAEntryType import IAEntryType
from TimeClock.Report.IAccess.IAMap import IAMap
from TimeClock.Report.IAccess.IAReport import IAReport
from TimeClock.Report.IAccess.IAReportData import IAReportData
from TimeClock.Report.IAccess.IASubAccount import IASubAccount
from TimeClock.Report.IAccess.IATimeEntry import IATimeEntry
from TimeClock.Report.IAccess.IAWorkLocation import IAWorkLocation
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible

interfaces = [
    IABenefit,
    IACalendarData,
    IAEmployee,
    IAEntryType,
    IAReport,
    IAReportData,
    IASubAccount,
    IATimeEntry,
    IAWorkLocation,
    IAMap,
    IDateTime,
    ITimeDelta
]

IDateTime.__bases__ += (IAbstractAccessible,)
ITimeDelta.__bases__ += (IAbstractAccessible,)
