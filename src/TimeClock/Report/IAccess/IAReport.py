from zope.interface import Attribute

from TimeClock.Report.IAccess.IAEmployee import IAEmployee
from TimeClock.Report.IAccess.IAReportData import IAReportData
from TimeClock.Report.IAccess.IAbstractAccessible import IAbstractAccessible
from TimeClock.Util import fromFunction
from TimeClock.Util.Overload import Overloader
from TimeClock.Utils import overload


class IAReport(IAbstractAccessible):
    """
    Main entry point for writing reports
    """

    formatterName = Attribute("formatterName")

    __overloader__ = Overloader()

    def getEmployees() -> [IAEmployee]:
        """
        Returns a generator which yields all employees (regardless of status)
        """

    @overload
    def formatRow(row: dict) -> bytes:
        """
        Adds a row to the report output, the serialized form of the row is returned
        """

    @fromFunction
    @overload
    def formatRow(row: IAReportData) -> bytes:
        """
        As above, but accepts anything which can be adapted to IAReportData
        """

    def formatHeader(columns: [str]) -> bytes:
        """
        Adds a header row to the report, columns are remembered for adding rows.
        Some formats require a header before rows may be added
        """

    def formatFooter() -> bytes:
        """
        Adds any footer information required to the report
        Required to output valid JSON and XML reports
        Automatically called once by reports that need it, call it when adding multiple tables to one report
        """

    def log(level, obj) -> None:
        """
        Formats and appends a row to the log area of the report widget
        """

    def print(*objs, **kw):
        """
        Shorthand for log('PRINT'...), formats output before logging.
        """

    def getInterfaces() -> [IAbstractAccessible]:
        """
        Returns a list of interfaces which allow attribute lookup and function calls
        """

    def timeDelta(**kw):
        """
        Creates a {ITimeDelta} object
        """

    def progress(progress):
        """
        Creates and updates a progress bar on the client running the report.  Range is 0...100 inclusive
        """

    def countEmployees() -> int:
        """
        Returns the total number of employees returned by getEmployees
        """

    del __overloader__
