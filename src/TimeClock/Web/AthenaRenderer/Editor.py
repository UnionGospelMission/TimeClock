from zope.interface import implementer

from TimeClock.ITimeClock.IWeb.IAthenaRenderable import IAthenaRenderable
from TimeClock.Web.AthenaRenderer.AbstractRenderer import AbstractRenderer, path
from nevow.athena import expose
from nevow.loaders import xmlfile


@implementer(IAthenaRenderable)
class Editor(AbstractRenderer):
    docFactory = xmlfile(path + "/Pages/Editor.xml", "AceEditor")
    jsClass = "TimeClock.Editor"
    name = 'Editor'
    def __init__(self, obj, attr, getter=getattr, setter=setattr):
        self.val = getter(obj, attr)
        self.obj = obj
        self.attr = attr
        self.setter = setter
        self.getter = getter
    @expose
    def revert(self):
        self.val = self.getter(self.obj, self.attr)
        return self.val
    @expose
    def save(self, newval, *args):
        self.setter(self.obj, self.attr, newval)
        self.val = newval
        if hasattr(self.parent, 'onSave'):
            self.parent.onSave(*args)
