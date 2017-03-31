from TimeClock.ITimeClock.IEvent.IEventBus import IEventBus
from TimeClock.Web.LiveFragmentMeta import LiveFragmentMeta
from nevow.athena import LiveFragment as LF
from nevow.stan import Tag

EventBus = None


class LiveFragment(LF, metaclass=LiveFragmentMeta):
    parent = None

    def detached(self):
        if self in self.instances:
            self.instances.remove(self)

        EventBus.unregister(self)

    def connectionLost(self, reason):
        self.detached()

    def child(self, ctx, idata):
        d = super().child(ctx, idata)
        return ctx, ctx.tag, d(ctx, idata)

    def locateMethod(self, ctx, methodName):
        try:
            method = super().locateMethod(ctx, methodName)
            return method
        except AttributeError as e:
            if methodName in self.api.getCommandShortNames():
                return getattr(self.api, methodName)
            raise e

    def __init__(self, *args, **kw):
        global EventBus
        EventBus = IEventBus("Web")
        super().__init__(*args, **kw)
        if self.fixCheckboxes not in self.preprocessors:
            self.preprocessors.append(self.fixCheckboxes)

    def setFragmentParent(self, parent):
        super().setFragmentParent(parent)
        self.instances.append(self)

    @staticmethod
    def fixCheckboxes(root: Tag):
        if not isinstance(root, (Tag, list, tuple)):
            return root
        if isinstance(root, (list, tuple)):
            for r in root:
                LiveFragment.fixCheckboxes(r)
            return root
        if root.tagName.lower() == "input" and 'type' in root.attributes and root.attributes['type'] == 'checkbox':
            if 'checked' in root.attributes and not root.attributes['checked']:
                del root.attributes['checked']
            elif 'value' in root.attributes and root.attributes['value'] is True:
                root.attributes['checked'] = ''
                del root.attributes['value']
        if root.tagName.lower() == 'option' and 'selected' in root.attributes and not root.attributes['selected']:
            del root.attributes['selected']
        for c in root.children:
            LiveFragment.fixCheckboxes(c)
        return root
    def preprocess(self, ret):
        for p in self.preprocessors:
            ret = p(ret)
        return ret

    def renderer(self, context, name):
        renderer = super().renderer(context, name)
        def flatten(ctx, data, _=None):
            if renderer.__code__.co_argcount==3:
                result = renderer(ctx, data)
            else:
                result = renderer(data)
            return self.preprocess(result)
        return flatten

