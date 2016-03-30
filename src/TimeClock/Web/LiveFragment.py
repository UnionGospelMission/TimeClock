from nevow.athena import LiveFragment


class LiveFragment(LiveFragment):
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
