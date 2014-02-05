#from distutils.core import setup
from setuptools import setup
import sys


REQUIRES = ['simplejson']

setup(name='cartodb_dashboard', 
      author = 'Simon Hope', 
      author_email = 'shope@geoplex.com.au',
      description = 'client to access cartodb dashboard',
      version='0.1',
      url='https://git.realestate.com.au/geodata/cartodb-dashboard-python',
      install_requires=REQUIRES,
      packages=['cartodb_dashboard'],
      requires = REQUIRES
)