#from distutils.core import setup
from setuptools import setup


REQUIRES = ['simplejson', 'httplib2', 'mako']

setup(name='cartodb_dashboard', 
      author = 'Simon Hope', 
      author_email = 'shope@geoplex.com.au',
      description = 'Provides access to the cartodb dashboard',
      version='0.2',
      url='https://github.com/realestate-com-au/cartodb-dashboard-python',
      download_url = 'https://github.com/realestate-com-au/cartodb-dashboard-python/tarball/0.2',
      install_requires=REQUIRES,
      packages=['cartodb_dashboard'],
      requires = REQUIRES,
      test_suite='test.client'
)