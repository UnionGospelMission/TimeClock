from setuptools import setup, find_packages
import datetime


setup(
    name='TimeClock',
    version='0.0.0.%s' % str(datetime.date.today()).replace('-', ''),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    entry_points={
        'console_scripts': ['axiomatic = TimeClock.Axiom.Axiomatic:run'],
    },
)
