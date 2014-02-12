[![Build Status](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python/badge/icon)](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python/)

cartodb-dashboard-python
========================

Python API for CartoDB Dashboard. Provides access to the following operations on the CartoDB API

+ Import table
+ Column data type changes
+ Delete table

<strong>IMPORTANT</strong>: This module works against a non published API which is subject to change. It has been tested without issue against the following CartoDB versions:

+ 2.3.2 - 2.9.1

# Requirements: 

+ Simplejson
+ httplib2

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
