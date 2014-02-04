#!/usr/bin/python
from cartodb import CartoDBDashboardException, CartoDbUtilities
import os

cartodb_api_key = os.environ['CARTODB_API_KEY']
cartodb_domain = os.environ['CARTDOB_DOMAIN']
cartodb_host = os.environ['CARTODB_HOST']
cartodb_protocol = os.environ['CARTODB_PROTOCOL']
cartodb_version = os.environ['CARTODB_VERSION']
cartodb_user = os.environ['CARTODB_USER']
cartodb_password = os.environ['CARTODB_PWD']

cl_util  = CartoDbUtilities(cartodb_domain,cartodb_user,cartodb_password,cartodb_host,cartodb_protocol,cartodb_version)

cl_util.import_data(file)



def update_data_types(column, datatype, table):
	try:
		cl_util.convert_data_type(column,datatype,table)
		return 0
	except CartoDBException as e:
	    print ("some error ocurred", e)
	    return 1


	
