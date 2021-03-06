from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Axiom.Store import Store
from TimeClock.Database.Commands.ManageWorkLocations import ManageWorkLocations as msa
from TimeClock.Database.WorkLocation import WorkLocation
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.AthenaRenderers.Commands import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderers.Widgets.List import List
from TimeClock.Web.AthenaRenderers.Widgets.SaveList import SaveList
from nevow.context import WovenContext
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ManageWorkLocations(AbstractCommandRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Commands'
    workLocations = None
    name = 'Manage Work Locations'
    def render_class(self, ctx, data):
        return "ManageWorkLocations"
    def render_genericCommand(self, ctx: WovenContext, data):
        l = List(list(Store.query(WorkLocation)), ['', "Work Location", "Description", "Active"])
        l.closeable = False
        l.addRow(SaveList(4, start=1))
        l.prepare(self)
        l.visible = True
        return l


registerAdapter(ManageWorkLocations, msa, IAthenaRenderable)
