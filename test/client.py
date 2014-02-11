import unittest
import os
from cartodb_dashboard import CartoDbDashboard


class CartoDbDashboardTest(object):
    def test_session_headers(self):
        result = self.client.request_session_headers
        self.assertIn('Cookie', result)

    def test_import_shapefile(self):
        result, table = self.client.import_data('test/testdata/localities.zip')
        self.assertTrue(result)

    def test_import_csv(self):
        result, table = self.client.import_data('test/testdata/schools.csv')
        self.assertTrue(result)

    def test_import_csv_update_column(self):
        result, table = self.client.import_data('test/testdata/schools.csv')
        self.assertTrue(result)
        self.assertTrue(self.client.convert_data_type("POINT_PID", "number", table))

    def test_get_table(self):
        result, table = self.client.import_data('test/testdata/schools.csv')
        self.assertTrue(result)
        table_res =  self.client.get_table(table)['table_visualization']['name']
        self.assertTrue(table,table_res)

    def test_delete_table(self):
        result, table = self.client.import_data('test/testdata/schools.csv')
        self.assertTrue(result)
        print self.client.delete_data(table)



class CartoDbDashboardTestClient(CartoDbDashboardTest, unittest.TestCase):
    def setUp(self):
        cartodb_domain = os.environ['CARTODB_DOMAIN']
        cartodb_host = os.environ['CARTODB_HOST']
        cartodb_protocol = os.environ['CARTODB_PROTOCOL']
        cartodb_version = os.environ['CARTODB_VERSION']
        cartodb_user = os.environ['CARTODB_USER']
        cartodb_password = os.environ['CARTODB_PWD']
        cartodb_api_port = os.environ['CARTODB_API_PORT']

        self.client = CartoDbDashboard(cartodb_domain, cartodb_user, cartodb_password, cartodb_host+':'+cartodb_api_port,cartodb_protocol,
                                       cartodb_version)

if __name__ == '__main__':
    unittest.main()

