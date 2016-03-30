from nevow.athena import expose

from TimeClock.Web.LiveFragment import LiveFragment
from nevow.loaders import xmlfile
from nevow.tags import br, input


path = __file__.rsplit('/', 2)[0]


class AbstractRenderer(LiveFragment):
    parent = None
    employee = None
    visible = False
    def prepare(self, parent: LiveFragment):
        self.parent = parent
        self.employee = parent.employee
        self.setFragmentParent(parent.fragmentParent)
        self.visible = hasattr(self.parent, "selectedElement") and self.parent.selectedElement == self
        return self
    @expose
    def getVisibility(self, Set=True):
        if Set:
            if self.visible:
                self.show()
            else:
                self.hide()
        return self.visible
    def render_visibility(self, ctx, idata):
        if self.visible:
            return "display:block"
        return "display:none"
    def hide(self):
        self.visible = False
        self.callRemote("hide");
    def show(self):
        self.visible = True
        self.callRemote("show");


