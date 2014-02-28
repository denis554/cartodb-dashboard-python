# -*- encoding: utf-8 -*-
from urllib import urlencode
from httplib2 import Http
from os import path
from mako.template import Template

try:
    import json
except ImportError:
    import simplejson as json

IMPORT_URL = '%(protocol)s://%(user)s.%(domain)s/api/%(api_version)s/imports'
SESSION_URL = '%(protocol)s://%(user)s.%(domain)s/sessions/create'
TABLES_URL = '%(protocol)s://%(user)s.%(domain)s/api/%(api_version)s/tables'
VIZ_URL = '%(protocol)s://%(user)s.%(domain)s/api/%(api_version)s/viz'


class CartoDBDashboardException(Exception):
    pass


class CartoDBTableInfo:
    def __init__(self, table_info_response):
        self.table_viz_id = table_info_response['table_visualization']['id']
        self.table_map_id = table_info_response['table_visualization']['map_id']
        self.table_privacy = table_info_response['table_visualization']['table']['privacy']
        self.table_id = table_info_response['table_visualization']['table']['id']
        self.table_size = table_info_response['table_visualization']['table']['size']
        self.table_row_count = table_info_response['table_visualization']['table']['row_count']
        self.updated_at = table_info_response['table_visualization']['table']['updated_at']
        self.created_at = table_info_response['table_visualization']['created_at']


class CartoDbDashboard:
    def __init__(self, cartodb_domain, user, password, host='cartodb.com', protocol='https', api_version='v1'):
        self.import_url = IMPORT_URL % {'user': cartodb_domain, 'domain': host, 'protocol': protocol,
                                        'api_version': api_version}
        self.session_url = SESSION_URL % {'user': cartodb_domain, 'domain': host, 'protocol': protocol}
        self.table_url = TABLES_URL % {'user': cartodb_domain, 'domain': host, 'protocol': protocol,
                                       'api_version': api_version}
        self.viz_url = VIZ_URL % {'user': cartodb_domain, 'domain': host, 'protocol': protocol,
                                  'api_version': api_version}
        self.client = Http()
        self.session_user = user
        self.session_password = password

    @property
    def request_session_headers(self):
        body = {'email': self.session_user, 'password': self.session_password}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = self.client.request(self.session_url, 'POST', headers=headers, body=urlencode(body))
        headers['Cookie'] = response['set-cookie']
        return headers

    def req(self, url, http_method="GET", http_headers={}, body=''):
        if http_method == "POST":
            resp, content = self.client.request(url, "POST", body=body, headers=http_headers)
        elif http_method == "PUT":
            resp, content = self.client.request(url, "PUT", body=body, headers=http_headers)
        elif http_method == "DELETE":
            resp, content = self.client.request(url, "DELETE", headers=http_headers)
        else:
            resp, content = self.client.request(url, "GET", headers=http_headers)

        if resp['status'] == '200':
            return json.loads(content)
        elif resp['status'] == '400':
            raise CartoDBDashboardException(json.loads(content))
        elif resp['status'] == '404':
            raise CartoDBDashboardException('Page Not Found')
        elif resp['status'] == '500':
            raise CartoDBDashboardException('internal server error')

        return None

    def __import_data(self, datafile):
        sessionbody = {'email': self.session_user, 'password': self.session_password}
        sessionheaders = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = self.client.request(self.session_url, 'POST', headers=sessionheaders, body=urlencode(sessionbody))

        def encode(file_path, fields=[]):
            boundary = '----------boundary------'
            crlf = '\r\n'
            encode_body = []

            for key, value in fields:
                encode_body.extend(
                    ['--{0}'.format(boundary),
                     'Content-Disposition: form-data; name="%s"' % key,
                     '',
                     value,
                    ])

            file_name = path.basename(file_path)
            f = open(file_path, 'rb')
            file_content = f.read()
            f.close()
            encode_body.extend(
                ['--' + boundary,
                 'Content-Disposition: form-data; name="file"; filename="%s"'
                 % file_name,
                 'Content-Type: application/octet-stream',
                 '',
                 file_content,
                ])

            encode_body.extend(['--' + boundary + '--', ''])
            return 'multipart/form-data; boundary=%s' % boundary, crlf.join(encode_body)

        content_type, body = encode(datafile)
        headers = {'Content-Type': content_type, 'Cookie': response['set-cookie']}

        return self.req(self.import_url, 'POST', http_headers=headers, body=body)['item_queue_id']

    def __convert_data_type(self, column, datatype, table):
        headers = self.request_session_headers
        body = {'name': column, 'type': datatype}
        url = self.table_url + '/' + table + '/columns/' + column
        return self.req(url, 'PUT', http_headers=headers, body=urlencode(body))

    def check_imports(self):
        headers = self.request_session_headers
        return self.req(self.import_url, 'GET', http_headers=headers)

    def check_import(self, importid):
        headers = self.request_session_headers
        return self.req(self.import_url + '/' + str(importid), 'GET', http_headers=headers)

    def convert_data_type(self, column, datatype, table):
        try:
            self.__convert_data_type(column, datatype, table)
            return True
        except CartoDBDashboardException as e:
            print ("some error occurred:", e)
            return False

    def import_data(self, datafile):
        try:
            importid = self.__import_data(datafile)
            res = None
            check = False
            while not check:
                res = self.check_import(importid)
                if res['state'] == 'uploading' or res['state'] == 'importing':
                    continue
                elif res['state'] == 'complete':
                    check = True

            return check, res['table_name']
        except CartoDBDashboardException as e:
            print ("some error occurred:", e)
            return False

    def get_table(self, table):
        try:
            headers = self.request_session_headers
            url = self.table_url + '/' + table
            return self.req(url, 'GET', http_headers=headers)
        except Exception as e:
            raise CartoDBDashboardException("An error occurred trying to get table information for table:" + table, e)

    def __delete_table(self, table_viz_id):
        headers = self.request_session_headers
        url = self.viz_url + '/' + table_viz_id
        return self.req(url, 'DELETE', http_headers=headers)

    def delete_data(self, table):
        try:
            #check the table exists and return the table viz id
            table_vis_id = self.get_table(table)['table_visualization']['id']
            #send delete command
            return self.__delete_table(table_vis_id)

        except CartoDBDashboardException as e:
            print ("some error occurred:", e)
            return False

    def rename_table(self, table_name, new_table_name):
        try:
            template = Template(
                '{"id": "${vis_id}", "name": "${table_name}", "map_id": ${map_id}, "type": "table", "tags": [], "description": null, "privacy": "${table_privacy}", "table": {"id": ${table_id}, "name": "${table_name}", "privacy": "${table_privacy}", "size": ${table_size}, "row_count": ${table_row_count}, "updated_at": "${updated_at}"}, "synchronization": null, "created_at": "${created_at}", "updated_at": "${updated_at}"}')
            table_info = CartoDBTableInfo(self.get_table(table_name))

            body = template.render(vis_id=table_info.table_viz_id, table_name=new_table_name, map_id=table_info.table_map_id,
                                   table_privacy=table_info.table_privacy, table_id=table_info.table_id, table_size=table_info.table_size, table_row_count=table_info
                                   .table_row_count, updated_at=table_info.updated_at, created_at=table_info.created_at)

            headers = self.request_session_headers
            url = self.viz_url + '/' + table_info.table_viz_id
            self.req(url, 'PUT', http_headers=headers, body=body)
            return True

        except CartoDBDashboardException as e:
            print ("some error occurred:", e)
            return False

