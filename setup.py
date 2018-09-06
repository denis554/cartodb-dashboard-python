#from distutils.core import setup
from setuptools import setup

VERSION  = '0.2.12'
REQUIRES = ['simplejson', 'httplib2']
URL      = 'https://github.com/realestate-com-au/cartodb-dashboard-python'

setup(name             = 'cartodb_dashboard',
      author           = 'Simon Hope',
      author_email     = 'shope@geoplex.com.au',
      description      = 'Provides access to the cartodb dashboard',
      version          = VERSION,
      url              = URL,
      download_url     = URL + '/tarball/' + VERSION,
      install_requires = REQUIRES,
      packages         = ['cartodb_dashboard'],
      requires         = REQUIRES,
      test_suite       = 'test.client'
)
