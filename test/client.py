import unittest
import os
from cartodb_dashboard import CartoDbDashboard


NEW_TABLE_NAME = 'test_table_can_delete'
TEMPLATE_PATH = '/templates/template_table_rename.json'
TEST_SHPFILE = 'test/testdata/localities.zip'
TEST_CSV = 'test/testdata/schools.csv'

class CartoDbDashboardTest(object):

    def test_session_headers(self):
        result = self.client.request_session_headers
        self.assertIn('Cookie', result)

    def test_import_shapefile(self):
        result, table = self.client.import_data(TEST_SHPFILE)
        self.assertTrue(result)
        if result:
            self.client.delete_data(table)

    def test_import_csv(self):
        result, table = self.client.import_data(TEST_CSV)
        self.assertTrue(result)
        if result:
            self.client.delete_data(table)

    def test_import_csv_update_column(self):
        result, table = self.client.import_data(TEST_SHPFILE)
        self.assertTrue(result)
        self.assertTrue(self.client.convert_data_type("POINT_PID", "number", table))
        if result:
            self.client.delete_data(table)

    def test_get_table(self):
        result, table = self.client.import_data(TEST_CSV)
        self.assertTrue(result)
        table_res =  self.client.get_table(table)['table_visualization']['name']
        self.assertTrue(table, table_res)
        if result:
            self.client.delete_data(table)

    def test_delete_table(self):
        result, table = self.client.import_data(TEST_CSV)
        self.assertTrue(result)
        self.client.delete_data(table)

    def test_rename_table(self):

        result, table = self.client.import_data(TEST_CSV)
        rename_success = self.client.rename_table(TEMPLATE_PATH, table, NEW_TABLE_NAME)
        self.assertTrue(rename_success)
        if rename_success:
            self.client.delete_data(NEW_TABLE_NAME)

class CartoDbDashboardTestClient(CartoDbDashboardTest, unittest.TestCase):
    def setUp(self):
        cartodb_domain = os.environ['CARTODB_DOMAIN']
        cartodb_host = os.environ['CARTODB_HOST']
        cartodb_protocol = os.environ['CARTODB_PROTOCOL']
        cartodb_version = os.environ['CARTODB_VERSION']
        cartodb_user = os.environ['CARTODB_USER']
        cartodb_password = os.environ['CARTODB_PWD']
        cartodb_api_port = os.environ['CARTODB_API_PORT']

        self.client = CartoDbDashboard(cartodb_domain, cartodb_user, cartodb_password, cartodb_host + ':' + cartodb_api_port, cartodb_protocol,
                                       cartodb_version)


if __name__ == '__main__':
    unittest.main()

