from nevow import inevow
from twisted.python.filepath import FilePath

from nevow.static import File
import TimeClock.Report.IAccess
import requests


class Reports(File):
    def __init__(self, *a, **kw):
        if not a and not kw:
            super().__init__(FilePath(TimeClock.Report.IAccess.__file__).parent().path)
        else:
            super().__init__(*a, **kw)

    def renderHTTP(self, ctx):
        req = inevow.IRequest(ctx)

        ret = super().renderHTTP(ctx)
        if req.method == 'HEAD':
            return ret
        if self.fp.path.endswith('py'):
            try:
                u = requests.post('http://hilite.me/api', data=dict(code=ret, linenos=True), timeout=1)
            except:
                return ret
            if 199 < u.status_code < 300:

                req.setHeader('content-type', 'text/html')

                ret = '''<html><body>%s</body></html>''' % u.text
                req.setHeader('content-length', len(ret))
        return ret
