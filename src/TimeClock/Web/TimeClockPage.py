from nevow.athena import LivePage
from .DocFactory import DocFactory


class RootPage(LivePage):
    docFactory = DocFactory()


