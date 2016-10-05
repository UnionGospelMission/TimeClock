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
        t = [
            self.currentPW,
            tags.input(id="newPassword", type="password", placeholder="New Password"),
            tags.br(),
            tags.input(id="newPasswordAgain", type="password", placeholder="New Password Again"),
            tags.br(),
            tags.input(value='Set Password', type='button')[tags.Tag('athena:handler')(event='onclick', handler='setPassword')]
        ]
        if self.employee is self._employee and self.employee.alternate_authentication and self.employee.alternate_authentication.expired and not self.employee.active_directory_name:
            t.insert(0, tags.h3(name='expired')['Your password is expired'])
        return self.preprocess(t)
    @expose
    @Transaction
    def setPassword(self, oldpassword, newpassword, newpassworda):
        if self._employee is self.employee and oldpassword is not None:
            expired = self._employee.alternate_authentication.expired
            self.args[0].execute(self._employee, oldpassword, newpassword, newpassworda)
            if expired:
                self.callRemote("logout")
        elif IAdministrator(self.employee):
            self.args[0].execute(IAdministrator(self.employee), self._employee, newpassword, newpassworda)

registerAdapter(SetPassword, TimeClock.Database.Commands.ChangeAuthentication.ChangeAuthentication, IAthenaRenderable)
