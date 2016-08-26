from TimeClock.Web.AthenaRenderers.Abstract.AbstractHideable import AbstractHideable
from TimeClock.Web.AthenaRenderers.Abstract.AbstractRenderer import AbstractRenderer, path
from TimeClock.Web.TimeClockStationPage import TimeClockStationPage
from nevow import tags
from nevow.athena import expose
from nevow.context import WovenContext
from nevow.loaders import xmlfile


class TimeClockStation(AbstractRenderer, AbstractHideable):
    docFactory = xmlfile(path + "/Pages/GenericCommand.xml", "GenericCommandPattern")
    jsClass = 'TimeClock.Widgets.TimeClockStation'
    visible = True
    name = 'Time Clock Station'
    def render_class(self, *a):
        return 'timeclockstation'
    def render_title(self, ctx, data):
        return "Time Clock - Station"
    def render_topLevel(self, *args):
        return 'timeClockStation' if self._topLevel else ""
    def render_genericCommand(self, ctx: WovenContext, data):
        return self.preprocess([tags.input(type='button', value='Start Time Clock Station')[tags.Tag('athena:handler')(event='onclick', handler='start')]])
    @expose
    def start(self):
        tcsPage = TimeClockStationPage()
        return tcsPage.pageId
    @expose
    def load(self, *a):
        pass
