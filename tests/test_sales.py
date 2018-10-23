"""Tests for get all sales"""
import json
import unittest
from app.api import sales


"""sale Request Response Tests"""


class TestEndPoints(unittest.TestCase):
    """Set Defaults"""

    def setUp(self):
        self.store_manager = app.app.test_client()
        self.path = '/api/v1'

    # The 4 main tests
    def test_get_sales(self):
        """return all entries: GET /api/v1/sales"""
        response = self.store_manager.get(self.path + '/sales')
        self.assertEqual(response.status_code, 200)

    def test_get_single_sale(self):
        """return specific sale"""
        _id = {"sale_id": 3}
        response = self.store_manager.get(self.path + '/sales/{}'.format(_id['sale_id']))
        self.assertEqual(response.status_code, 200)

    def test_post_new_sale(self):
        """create new sale"""
        response = self.store_manager.post(self.path + '/sales',
                                      data=json.dumps(dict(title='Macbook pro', serial='MCP12345', cost=120000, attendant='Good working condition')),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_sale(self):
        """delete specific sale"""
        _id = {"sale_id": 1}
        response = self.store_manager.delete(self.path + '/sales/{}'.format(_id['sale_id']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', str(response.data))

    def test_put_update_sale(self):
        """update sale if the sale_id exist"""
        response = self.store_manager.put(self.path + '/sales/3', data=json.dumps(
            dict(title='Macbook pro', serial='Mpc54321', cost=120000, attendant='Faulty')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_new_sale(self):
        """create new sale if the id doesn't exist"""
        response = self.store_manager.put(self.path + '/sales/6',
                                     data=json.dumps(dict(title='Macbook pro', serial='MCP12345', cost=120000, attendant='Good working condition')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_non_existing_sale(self):
        """return status code 404 (when sale not found)"""
        _id = {"sale_id": 233}
        response = self.store_manager.get(self.path + '/sale/{}'.format(_id['sale_id']))
        self.assertEqual(response.status_code, 404)

    def test_get_sale_missing_id(self):
        """reject request looking for a sale but lacking an saleID"""
        _id = {"sale_id": None}
        response = self.store_manager.get(self.path + '/sales/{}'.format(_id['sale_id']))
        self.assertEqual(response.status_code, 404)

    def test_get_sale_non_integer_id(self):
        """reject request looking for a sale but lacking numerical saleID"""
        _id = {"sale_id": 'home'}
        response = self.store_manager.get(self.path + '/sales/{}'.format(_id['sale_id']))
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)