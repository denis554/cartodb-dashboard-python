#from distutils.core import setup
from setuptools import setup

VERSION  = '0.2.3'
REQUIRES = ['simplejson', 'httplib2']

setup(name             = 'cartodb_dashboard',
      author           = 'Simon Hope',
      author_email     = 'shope@geoplex.com.au',
      description      = 'Provides access to the cartodb dashboard',
      version          = VERSION,
      url              = 'https://github.com/realestate-com-au/cartodb-dashboard-python',
      download_url     = 'https://github.com/realestate-com-au/cartodb-dashboard-python/tarball/' + VERSION,
      install_requires = REQUIRES,
      packages         = ['cartodb_dashboard'],
      requires         = REQUIRES,
      test_suite       = 'test.client'
)
