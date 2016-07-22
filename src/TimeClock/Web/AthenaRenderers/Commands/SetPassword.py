from twisted.python.components import registerAdapter

import TimeClock.Database.Commands
from TimeClock.Axiom import Transaction
from TimeClock.ITimeClock.IDatabase.IAdministrator import IAdministrator
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


class SetPassword(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands.SetPassword'
    subaccounts = None
    name = 'Set Password'
    _employee = None
    currentPW = [tags.input(id="currentPassword", type="password", placeholder="Current Password"),
                 tags.br()]
    def prepare(self, parent, force: bool=False):
        super().prepare(parent, force)
        self._employee = self.employee
    def render_genericCommand(self, ctx: WovenContext, data):
        return self.preprocess([
            self.currentPW,
            tags.input(id="newPassword", type="password", placeholder="New Password"),
            tags.br(),
            tags.input(id="newPasswordAgain", type="password", placeholder="New Password Again"),
            tags.br(),
            tags.input(value='Set Password', type='button')[tags.Tag('athena:handler')(event='onclick', handler='setPassword')]
        ])
    @expose
    @Transaction
    def setPassword(self, oldpassword, newpassword, newpassworda):
        if self._employee is self.employee and oldpassword is not None:
            self.args[0].execute(self._employee, oldpassword, newpassword, newpassworda)
        elif IAdministrator(self.employee):
            self.args[0].execute(IAdministrator(self.employee), self._employee, newpassword, newpassworda)

registerAdapter(SetPassword, TimeClock.Database.Commands.ChangeAuthentication.ChangeAuthentication, IAthenaRenderable)
