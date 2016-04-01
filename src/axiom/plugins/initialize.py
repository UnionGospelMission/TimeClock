import importlib

from axiom.iaxiom import IAxiomaticCommand
from axiom.scripts import axiomatic

from zope.interface import provider

from twisted.python import usage
from twisted.plugin import IPlugin
from TimeClock.initialize import initialize






class Options(usage.Options):
    optParameters = [
        ["username", "u", None, "Active directory username to use to lookup employee information in LDAP"],
        ["password", "p", None, "LDAP password"],
    ]


@provider(IPlugin, IAxiomaticCommand)
class PrintAllItems(Options, axiomatic.AxiomaticSubCommandMixin):

    # This is how it will be invoked on the command line
    name = "initialize-timeclock"

    # This will show up next to the name in --help output
    description = "Initializes the database with an administrator and tries to find AD names for new employees"


    def postOptions(self):
        s = self.parent.getStore()

        initialize(s, self)


