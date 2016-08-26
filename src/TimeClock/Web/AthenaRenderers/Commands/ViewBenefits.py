from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database import Commands
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Solomon import Solomon
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ViewBenefits(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    name = 'View Benefits'
    loaded = False
    @expose
    def load(self):
        pass
    l = None
    def render_genericCommand(self, ctx: WovenContext, data):
        self.l = l = List(list(self.getEntries()), ["Benefit", "Beginning Balance", "Accrued", "Used", "Available"])
        l.closeable = False
        l.prepare(self)
        l.visible = True
        return l
    def getEntries(self):
        benefits = Solomon.getBenefits(self.employee)
        o = []
        for b in benefits:
            begin = b['BYBegBal']
            accrued = b['BYTDAvail']
            used = b['BYTDUsed']
            avail = begin + accrued - used
            name = Solomon.getBenefit(b['BenId'])['Descr']
            o.append([name, "%.2f" % begin, "%.2f" % accrued, "%.2f" % used, "%.2f" % avail])
        return o

registerAdapter(ViewBenefits, Commands.ViewBenefits.ViewBenefits, IAthenaRenderable)
