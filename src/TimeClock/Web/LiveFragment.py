from nevow.athena import LiveFragment
from nevow.stan import Tag


class LiveFragment(LiveFragment):
    parent = None
    def child(self, ctx, idata):
        d = super(LiveFragment, self).child(ctx, idata)
        return ctx, ctx.tag, d(ctx, idata)
    def locateMethod(self, ctx, methodName):
        try:
            method = super(LiveFragment, self).locateMethod(ctx, methodName)
            return method
        except AttributeError as e:
            if methodName in self.api.getCommandShortNames():
                return getattr(self.api, methodName)
            raise e
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        if self.fixCheckboxes not in self.preprocessors:
            self.preprocessors.append(self.fixCheckboxes)
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
        for c in root.children:
            LiveFragment.fixCheckboxes(c)
        return root
    def preprocess(self, ret):
        for p in self.preprocessors:
            ret = p(ret)
        return ret

