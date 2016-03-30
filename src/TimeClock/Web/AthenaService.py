import importlib

import twisted
from twisted.internet import ssl

import TimeClock
from nevow.appserver import NevowSite
from twisted.application.service import IServiceCollection
from twisted.internet import reactor

from axiom.attributes import text

from axiom.attributes import integer, reference

from axiom.item import Item
from zope.interface import implementer

from .PageFactory import PageFactory


@implementer(twisted.application.service.IService)
class AthenaService(Item):
    port = integer()
    iajs_fqpn = text()
    name = text()
    parent = reference()
    factory = reference()
    @property
    def iajs(self):
        importlib.import_module(self.iajs_fqpn)
        return importlib.import_module(self.iajs_fqpn, self.iajs_fqpn)
    @staticmethod
    def new(options):
        self = AthenaService()
        self.port = options.get('port', None)
        self.iajs_fqpn = options['iajs']
        return self
    def installOn(self, store):
        self.store=store
        store.powerUp(self, twisted.application.service.IService)
    def setName(self, name):
        if self.parent:
            raise RuntimeError("Cannot set name after parent")
        self.name = name
    def setServiceParent(self, parent):
        IServiceCollection(parent).addService(self)
        if isinstance(parent, Item):
            self.parent = parent
    def disownServiceParent(self, parent):
        return self.parent.removeService(self)
    def startService(self):
        pf = PageFactory(self.iajs, self.port)
        for i in pf.iajs.Ports:
            if i[0]=='TCP':
                reactor.listenTCP(i[1], NevowSite(pf))
                continue
            if i[0]=='UDP':
                reactor.listenUDP(i[1], NevowSite(pf))
                continue
            if i[0]=='SSL':
                reactor.listenSSL(i[1], ssl.DefaultOpenSSLContextFactory(
                    self.options['key'], self.options['crt']), pf)

    def stopService(self):
        return
    def privilegedStartService(self):
        return
