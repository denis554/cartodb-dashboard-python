# -*- encoding: utf-8 -*-

from httplib2 import Http

import os
import urllib
import urllib2
import base64
import json
import sys
import argparse
import time


try:
    import requests
except ImportError:
    print 'The requests package is required: http://docs.python-requests.org/en/latest/user/install/#install'
    sys.exit()


try:
    import json
except ImportError:
    import simplejson as json

SQL_URL = "%(protocol)s://%(user)s.%(domain)s/api/%(sql_version)s/sql"
IMPORT_URL = '%(protocol)s://%(user)s.%(domain)s/api/%(import_version)s/imports/%(queue_id)s?api_key=%(api_key)s'



class CartoDBDashboardException(Exception):
    pass



class CartoDbDashboard:
    def __init__(self, user, key, host='carto.com', protocol='https', sql_version='v2', import_version='v1', verbose=True):

        self.user = user
        self.key = key
        self.host = host
        self.protocol = protocol
        self.sql_version = sql_version
        self.import_version = import_version
        self.verbose = verbose

        self.sql_url = SQL_URL % {'user': user, 'domain': host, 'protocol': protocol, 'sql_version': sql_version}
        self.import_url = IMPORT_URL % {'user': user, 'domain': host, 'protocol': protocol,'import_version': import_version, 'api_key': key, 'queue_id':''}


    def _log(self, message):
        if self.verbose == True:
            print message

    def _error(self, error):
        print error
        sys.exit()

    def sql_api(self, sql):
        # execute sql request over API
        try:
            params = {
                'api_key' : self.key,
                'q'       : sql
            }
            r = requests.get(self.sql_url, params=params)
            return r.json()
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))


    def convert_data_type(self, column, coltype, table):
        try:
            if coltype == 'string':
                coltype = 'text'
            elif coltype == 'number':
                coltype = 'numeric USING NULLIF( %s , \'\')::numeric' %(column)

            sql = "ALTER TABLE %s ALTER COLUMN %s TYPE %s" % (table, column, coltype)
            data = self.sql_api(sql)
            return True
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False



    def import_data(self, datafile, type_guessing = 'true'):
        try:
            self._log('NEW..')
            params = {
                'type_guessing' : type_guessing
            }

            r = requests.post(self.import_url, files={'file': open(datafile, 'rb')}, params=params)

            data = r.json()
            if data['success']!=True:
                self._error("Upload failed")
            complete = False
            last_state = ''
            while not complete:
                import_status_url = IMPORT_URL % {'user': self.user, 'domain': self.host, 'protocol': self.protocol, 'sql_version': self.sql_version, 'import_version': self.import_version, 'api_key': self.key,'queue_id':data['item_queue_id']}
                req = urllib2.Request(import_status_url)
                response = urllib2.urlopen(req)
                d = json.loads(str(response.read()))
                if last_state!=d['state']:
                    last_state=d['state']
                    if d['state']=='uploading':
                        self._log('Uploading file...')
                    elif d['state']=='importing':
                        self._log('Importing data...')
                    elif d['state']=='complete':
                        if d['success']==True:
                            complete = True
                            self._log('Table "%s" created' % d['table_name'])
                            return complete,d['table_name']
                        else:
                            self._error(d['get_error_text']['what_about'])

                if d['state']=='failure':
                    self._error(d['get_error_text']['what_about'])

        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False


    def drop_table(self, table):
        # drop a table '
        try:
            self._log("Dropping table %s"  % table)
            sql = "DROP TABLE %s" % table
            data = self.sql_api(sql)
            if 'error' in data.keys():
                self._error(data['error'])
            return True
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False

    def clear_rows(self, table):
        # clear all rows from a table
        try:
            self._log("Deleting all rows")
            sql = "DELETE FROM %s" % table
            data = self.sql_api(sql)
            if 'error' in data.keys():
                self._error(data['error'])
            return True
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False


    def clean_table(self,table):
        # clean up table for speed
        try:
            self._log("Cleaning up unused space")
            sql = "VACUUM FULL %s" % table
            data = self.sql_api(sql)
            if 'error' in data.keys():
                self._error(data['error'])
            self._log("Optimizing existing indexes")
            sql = "ANALYZE %s" % table
            data = self.sql_api(sql)
            if 'error' in data.keys():
                self._error(data['error'])
            return True
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False


    def get_row_count(self,table):
        try:
            count = -1
            sql = "SELECT count(*) FROM %s" % table
            data = self.sql_api(sql)
            if data:
                if 'error' in data.keys():
                    return count
                count = data['rows'][0]['count']
            return count
        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return 0

    def rename_table(self, table_name, new_table_name):
        print "Start renaming process by a little wait of 30s from %s" % time.ctime()
        time.sleep( 60 )
        print "Hopefully we are now good to go"

        try:
            if self.table_exists(table_name):
                sql = "ALTER TABLE %s  RENAME TO %s" % (table_name, new_table_name)
                data = self.sql_api(sql)
                if 'error' in data.keys():
                    self._error(data['error'])
                return True
            return False

        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False


    def table_exists(self, table_name):
        try:
            if self.get_row_count(table_name) >=0:
                return True
            return False

        except CartoDBDashboardException as e:
            self._log('some error occurred: %s' %(e))
            return False
