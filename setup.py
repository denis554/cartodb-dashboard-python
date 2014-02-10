#from distutils.core import setup
from setuptools import setup


REQUIRES = ['simplejson', 'httplib2']

setup(name='cartodb_dashboard', 
      author = 'Simon Hope', 
      author_email = 'shope@geoplex.com.au',
      description = 'Provides access to the cartodb dashboard',
      version='0.1',
      url='https://git.realestate.com.au/geodata/cartodb-dashboard-python',
      download_url = 'https://git.realestate.com.au/geodata/cartodb-dashboard-python/tarball/0.1',
      install_requires=REQUIRES,
      packages=['cartodb_dashboard'],
      requires = REQUIRES,
      test_suite='test.client'
)