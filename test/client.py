import unittest
import os
from cartodb_dashboard import CartoDbDashboard


NEW_TABLE_NAME = 'test_table_can_delete'
TEST_SHPFILE = 'test/testdata/localities.zip'
TEST_CSV = 'test/testdata/schools.csv'

class CartoDbDashboardTest(object):

    def test_import_shapefile(self):
        result, table = self.client.import_data(TEST_SHPFILE)
        self.assertTrue(result)
        if result:
            self.client.drop_table(table)

    def test_import_csv(self):
        result, table = self.client.import_data(TEST_CSV)
        self.assertTrue(result)
        if result:
            self.client.drop_table(table)

    def test_import_csv_update_column(self):
        result, table = self.client.import_data(TEST_CSV)
        self.assertTrue(result)
        self.assertTrue(self.client.convert_data_type("POINT_PID", "number", table))
        if result:
            self.client.drop_table(table)


    def test_delete_table(self):
        result, table = self.client.import_data(TEST_CSV)        
        self.assertTrue(self.client.drop_table(table))

    def test_rename_table(self):
        result, table = self.client.import_data(TEST_CSV)
        rename_success = self.client.rename_table(table, NEW_TABLE_NAME)
        self.assertTrue(rename_success)
        if rename_success:
            self.client.drop_table(NEW_TABLE_NAME)

    def test_rename_table_that_does_not_exist(self):
        rename_success = self.client.rename_table("doesnotexist", "hardluck")
        self.assertFalse(rename_success)

    def test_table_exists(self):
        try:
          status,table =self.client.import_data(TEST_CSV)
          result = self.client.table_exists(table)
          self.assertTrue(table)

        finally:
            self.client.drop_table(table)

    def test_table_exists_when_table_does_not_exist(self):
        result = self.client.table_exists('doesnotexist')
        self.assertFalse(result)


class CartoDbDashboardTestClient(CartoDbDashboardTest, unittest.TestCase):
    def setUp(self):
        cartodb_user = os.environ['CARTODB_USER']
        cartodb_api_key = os.environ['CARTODB_API_KEY'] 

        self.client = CartoDbDashboard(cartodb_user,cartodb_api_key)


if __name__ == '__main__':
    unittest.main()

