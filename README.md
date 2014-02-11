[![Build Status](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python/badge/icon)](https://buildhive.cloudbees.com/job/realestate-com-au/job/cartodb-dashboard-python//)

cartodb-dashboard-python
========================

Python API for CartoDB Dashboard. Provides access to the following operations on the CartoDB API

+ Import
+ Column data type changes

# Requirements: 

+ Simplejson
+ httplib2

# Install

+ clone repo
+ cd to cloned directory

```bash
python setup.py install
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