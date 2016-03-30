import importlib

from TimeClock.Web.AthenaService import AthenaService

from axiom.iaxiom import IAxiomaticCommand
from axiom.scripts import axiomatic

from zope.interface import provider

from twisted.python import usage
from twisted.plugin import IPlugin







class Options(usage.Options):
    optParameters = [
        ["port", "p", None, "The port number on which to listen, overrides IAthenaJS and assumes TCP."],
        ["iajs", "i", "ajs", "The fully qualified python name of a module which contains an implementor of IAthenaJS"
                             "or something adaptable to IAthenaJS"],
        ["key", "k", None, "Filename for server.key for ssl"],
        ["crt", "c", None, "Filename for server.crt for ssl"]
    ]


@provider(IPlugin, IAxiomaticCommand)
class PrintAllItems(Options, axiomatic.AxiomaticSubCommandMixin):

    # This is how it will be invoked on the command line
    name = "install-athena-server"

    # This will show up next to the name in --help output
    description = "Installs an athena server provided by iajs on the store"


    def postOptions(self):
        s = self.parent.getStore()
        AthenaService.new(self).installOn(s)


