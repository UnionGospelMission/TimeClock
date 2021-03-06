from setuptools import setup
from twisted.python.filepath import FilePath as FP

def getAll(root, *branches):
    if isinstance(root, str):
        root = FP(root)
    o = []
    for branch in branches:
        if isinstance(branch, str):
            fp = root.child(branch)
        else:
            fp = branch
        if fp.isdir():
            o.extend(getAll(root, *fp.children()))
        else:
            o.append('/'.join(fp.segmentsFrom(root)))
    return o


setup(
    name='TimeClock',
    version='0.9.0',
    requires=['zope.interface', 'arrow', 'pymssql', 'ldap3', 'pytz', 'tzlocal', 'zope.component', 'cffi', 'pyOpenSSL',
              'service_identity', 'ptpython', 'html5print'],
    packages=['', 'TimeClock', 'TimeClock.AD', 'TimeClock.API', 'TimeClock.Web', 'TimeClock.Web.Events',
              'TimeClock.Web.AthenaRenderers', 'TimeClock.Web.AthenaRenderers.Objects',
              'TimeClock.Web.AthenaRenderers.Widgets', 'TimeClock.Web.AthenaRenderers.Abstract',
              'TimeClock.Web.AthenaRenderers.Commands', 'TimeClock.Web.AthenaRenderers.TimeClockStationWidgets',
              'TimeClock.Util', 'TimeClock.Axiom', 'TimeClock.Event', 'TimeClock.Report', 'TimeClock.Report.Format',
              'TimeClock.Sandbox', 'TimeClock.Solomon', 'TimeClock.Database', 'TimeClock.Database.API',
              'TimeClock.Database.Event', 'TimeClock.Database.Commands', 'TimeClock.Database.Reflection',
              'TimeClock.PTPython', 'TimeClock.ITimeClock', 'TimeClock.ITimeClock.IWeb', 'TimeClock.ITimeClock.IEvent',
              'TimeClock.ITimeClock.IEvent.IWebEvent', 'TimeClock.ITimeClock.IEvent.IDatabaseEvent',
              'TimeClock.ITimeClock.IReport', 'TimeClock.ITimeClock.IDatabase'],
    package_dir={'': 'src'},
    package_data={'TimeClock.Web': getAll('src/TimeClock/Web/', 'JS', 'CSS', 'Pages')},
    url='',
    license='',
    author='',
    author_email='',
    description='',
    scripts=['bin/axiomatic']
)
