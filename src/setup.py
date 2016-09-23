from distutils.core import setup

setup(
    name='TimeClock',
    version='0.9.0',
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
    package_dir={'': 'TimeClock/src'},
    url='',
    license='',
    author='',
    author_email='',
    description=''
)
