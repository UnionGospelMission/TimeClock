from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from nevow.context import WovenContext


class IListRow(IAthenaRenderable):
    def render_listRow(ctx: WovenContext, data):
        pass
