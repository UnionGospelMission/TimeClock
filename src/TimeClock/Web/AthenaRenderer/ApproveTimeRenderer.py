from twisted.python.components import registerAdapter
from zope.interface import implementer

from TimeClock.Database.Commands.ApproveTime import ApproveTime
from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractCommandRenderer import AbstractCommandRenderer
from TimeClock.Web.AthenaRenderer.AbstractRenderer import path
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class ApproveTimeRenderer(AbstractCommandRenderer):
    docFactory = xmlfile(path + '/Pages/ApproveHours.xml')
    jsClass = 'TimeClock.ApproveHours'


registerAdapter(ApproveTimeRenderer, ApproveTime, IAthenaRenderable)
