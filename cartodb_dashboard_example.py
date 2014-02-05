#!/usr/bin/python
from cartodb_dashboard import CartoDBDashboardException, CartoDbDashboard
import os
import argparse
import json

#Grab properties from environment
cartodb_api_key = os.environ['CARTODB_API_KEY']
cartodb_domain = os.environ['CARTDOB_DOMAIN']
cartodb_host = os.environ['CARTODB_HOST']
cartodb_protocol = os.environ['CARTODB_PROTOCOL']
cartodb_version = os.environ['CARTODB_VERSION']
cartodb_user = os.environ['CARTODB_USER']
cartodb_password = os.environ['CARTODB_PWD']

def run(file, conversions):

	#create instance of the utilities 
	cl_db  = CartoDbDashboard(cartodb_domain,cartodb_user,cartodb_password,cartodb_host,cartodb_protocol,cartodb_version)

	#run import and data type conversion
	res = cl_db.import_data(file)
	new_table = res[1]

	#iterate over columns/data types
	if conversions is not None:
		for key in conversions.iterkeys():
			success = cl_db.convert_data_type(key,conversions[key],new_table)


if __name__ == '__main__':

	#grab the args
	parser = argparse.ArgumentParser(description='Import file to CartoDB')
	parser.add_argument('file', metavar='file', type=str, help='Path to import file')
	parser.add_argument('conversions', metavar='conversions', nargs='?', type=json.loads, help='Json dictionary of data type converions')


	args = parser.parse_args()
	file = args.file
	dt_conversions = args.conversions

	run(file,dt_conversions)	



	
