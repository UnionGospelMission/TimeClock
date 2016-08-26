
from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.ManageSubAccounts import ManageSubAccounts as msa
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ManageSubAccounts(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/ManageSubAccounts.xml", "ManageSubAccountsPattern")
    jsClass = 'TimeClock.Commands'
    subaccounts = None
    name = 'Manage Sub Accounts'
    def render_subAccounts(self, ctx: WovenContext, data):
        l = List(list(Store.query(SubAccount)), ["", "Sub Account", "Name", "Active"])
        l.closeable = False
        l.addRow(SaveList(4, start=1))
        l.prepare(self)
        l.visible = True
        return l


registerAdapter(ManageSubAccounts, msa, IAthenaRenderable)
