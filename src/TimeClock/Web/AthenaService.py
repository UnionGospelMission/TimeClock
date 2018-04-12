import importlib

from OpenSSL import SSL
from OpenSSL import crypto

import twisted
from TimeClock.Web.CipherEntry import ICipherEntry, CipherEntry
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

ports = {}


@implementer(twisted.application.service.IService)
class AthenaService(Item):
    schemaVersion = 4
    port = integer()
    iajs_fqpn = text()
    name = text()
    parent = reference()
    factory = reference()
    certificate = text()
    chain_file = text(default='/home/timeclock/chain.crt')
    dhparam_file = text(default='/home/timeclock/dhparams.pem')
    ec_name = text(default='prime256v1')
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
        self.addCipherEntry('DEFAULT')

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
            if i[0] == 'TCP':
                ports[self.storeID] = [reactor.listenTCP(i[1], NevowSite(pf))]
                continue
            if i[0] == 'UDP':
                ports[self.storeID] = [reactor.listenUDP(i[1], NevowSite(pf))]
                continue
            if i[0] == 'SSL':
                ctx = ssl.DefaultOpenSSLContextFactory(
                    self.privkey, self.certificate, SSL.TLSv1_2_METHOD)
                ctx._context.load_tmp_dh(self.dhparam_file)

                ctx._context.set_tmp_ecdh(crypto.get_elliptic_curve(self.ec_name))
                ctx._context.set_options(SSL.OP_NO_TLSv1)
                ctx._context.set_options(SSL.OP_NO_TLSv1_1)
                ctx._context.use_certificate_chain_file(self.chain_file)
                ctx._context.set_cipher_list(self.getCiphers())
                ctx._context.set_options(SSL.OP_SINGLE_DH_USE)


                factory = NevowSite(pf)
                port = reactor.listenSSL(i[1], factory, ctx)
                ports[self.storeID] = [port, ctx]

    def stopService(self):
        ports[self.storeID][0].stopListening()

    def getCiphers(self):
        return str.join(':', [i.entry for i in self.powerupsFor(ICipherEntry)])

    def privilegedStartService(self):
        return

    def addCipherEntry(self, entry: str):
        self.powerUp(CipherEntry(store=self.store, entry=entry), ICipherEntry)

    def removeCipherEntry(self, entry: str):
        for i in self.powerupsFor(ICipherEntry):
            if i.entry == entry:
                self.powerDown(i, ICipherEntry)

registerAttributeCopyingUpgrader(
    AthenaService,
    1,
    2
)

registerAttributeCopyingUpgrader(
    AthenaService,
    2,
    3
)

registerAttributeCopyingUpgrader(
    AthenaService,
    3,
    4
)
