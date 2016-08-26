import importlib

import twisted
from twisted.internet.protocol import Factory

from axiom.upgrade import registerAttributeCopyingUpgrader
from twisted.internet import ssl

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
    schemaVersion = 2
    port = integer()
    iajs_fqpn = text()
    name = text()
    parent = reference()
    factory = reference()
    certificate = text()
    privkey = text()
    protocol = text(default='TCP')
    @property
    def iajs(self):
        importlib.import_module(self.iajs_fqpn)
        return importlib.import_module(self.iajs_fqpn, self.iajs_fqpn)
    @staticmethod
    def new(options):
        self = AthenaService()
        port = options.get('port', None)
        proto = options.get('protocol', 'TCP')
        cert = options.get('certificate', None)
        pkey = options.get('privkey', None)
        if port:
            self.port = int(port)
        if proto:
            self.protocol = proto
        if cert:
            self.certificate = cert
        if pkey:
            self.privkey = pkey
        self.iajs_fqpn = options['iajs']
        return self
    def installOn(self, store):
        self.store = store
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
        from ..PTPython import embed
        embed()

        pf = PageFactory(self.iajs, self.port, self.protocol)
        for i in pf.iajs.Ports:
            if i[0]=='TCP':
                reactor.listenTCP(i[1], NevowSite(pf))
                continue
            if i[0]=='UDP':
                reactor.listenUDP(i[1], NevowSite(pf))
                continue
            if i[0]=='SSL':
                factory = NevowSite(pf)
                reactor.listenSSL(i[1], factory, ssl.DefaultOpenSSLContextFactory(
                    self.privkey, self.certificate))

    def stopService(self):
        return
    def privilegedStartService(self):
        return

registerAttributeCopyingUpgrader(
    AthenaService,
    1,
    2
)
