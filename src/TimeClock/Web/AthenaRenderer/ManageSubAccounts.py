from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.SubAccount import SubAccount
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from nevow import inevow, tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ManageSubAccounts(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/ManageSubAccounts.xml", "ManageSubAccountsPattern")
    jsClass = 'TimeClock.SubAccounts'
    subaccounts = None
    name = 'Manage Sub Accounts'
    def render_listSubAccounts(self, ctx: WovenContext, data):
        listRow = inevow.IQ(ctx).patternGenerator("listRow")
        o = []
        self.subaccounts = list(Store.query(SubAccount))
        for idx, i in enumerate(self.subaccounts):
            inp = tags.input(type='checkbox', **{'data-storeid': i.storeID})[
                tags.Tag("athena:handler")(event='onchange', handler='toggleActive')
            ]
            if i.active:
                inp(checked='checked')
            inp = [inp]
            for p in self.preprocessors:
                inp = p(inp)
            o.append(listRow(data=dict(index=i.storeID,
                                       subAccountName=i.name,
                                       subAccountID='%05i' % i.sub,
                                       subAccountVisible=inp,
                                       searchclass='subAccount')))
        for i in self.preprocessors:
            o = i(o)
        return o
    @expose
    def toggleActive(self, storeID, active):
        adm = IAdministrator(self.employee)
        sub = Store.getItemByID(int(storeID))
        if not isinstance(sub, SubAccount):
            return
        print(41, adm, sub, active)
        sub.active = active
