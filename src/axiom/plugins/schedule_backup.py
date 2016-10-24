import importlib

from TimeClock.Util.BackupTask import BackupTask
from axiom.iaxiom import IAxiomaticCommand
from axiom.scripts import axiomatic

from zope.interface import provider

from twisted.python import usage
from twisted.plugin import IPlugin






class Options(usage.Options):
    optParameters = [
        ["destination", "d", None, "Destination of backup file"],
        ["when", "w", None, "Time of day to create backups"],
    ]


@provider(IPlugin, IAxiomaticCommand)
class ScheduleBackup(Options, axiomatic.AxiomaticSubCommandMixin):

    # This is how it will be invoked on the command line
    name = "schedule-backup"

    # This will show up next to the name in --help output
    description = "Schedule daily backups of database"

    def postOptions(self):
        s = self.parent.getStore()
        BackupTask.new(self).installOn(s)


