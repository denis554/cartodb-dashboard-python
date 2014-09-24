[![Build Status](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python/badge/icon)](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python/)

cartodb-dashboard-python
========================

Python API for CartoDB Dashboard. Provides access to the following operations on the CartoDB API

+ Import table
+ Column data type changes
+ Delete table
+ Rename table

<strong>IMPORTANT</strong>: This module works against a non published API which is subject to change. It has been tested without issue against the following CartoDB versions:

| Cartodb Dashboard Client Version   | CartoDB Version |
|----------|:-------------:|
| < 0.2.1 | 2.3.0 -  2.9.1   |


# Requirements:

+ Simplejson
+ httplib2
+ mako

# Install

+ clone repo
+ cd to cloned directory

```bash
python setup.py install
```

Or you can install from PyPi

```bash
pip install cartodb_dashboard
```

# Usage

```python
client = CartoDbDashboard(cartodb_domain, cartodb_user, cartodb_password, cartodb_host+':'+cartodb_api_port,
cartodb_protocol, cartodb_version)
client.import_data('test/testdata/localities.zip')
```


# Tests

+ clone repo
+ cd to cloned directory

```bash
python setup.py test
```

# Publish to PyPi
You will need an account on [PyPi](https://pypi.python.org/pypi) to be able to publish a new version of this package.

## Register and upload
`python setup.py sdist register upload`

## Install locally
The new version should be available for install as per the "Install from PyPi" section above.
