"""Tests for get all products"""
import json
import unittest
from app.api import products


"""product Request Response Tests"""


class TestEndPoints(unittest.TestCase):
    """Set Defaults"""

    def setUp(self):
        self.store_manager = app.app.test_client()
        self.path = '/api/v1'

    # The 4 main tests
    def test_get_products(self):
        """return all entries: GET /api/v1/products"""
        response = self.store_manager.get(self.path + '/products')
        self.assertEqual(response.status_code, 200)

    def test_get_single_product(self):
        """return specific product"""
        _id = {"product_id": 3}
        response = self.store_manager.get(self.path + '/products/{}'.format(_id['product_id']))
        self.assertEqual(response.status_code, 200)

    def test_post_new_product(self):
        """create new product"""
        response = self.store_manager.post(self.path + '/products',
                                      data=json.dumps(dict(title='Macbook pro', serial='MCP12345', Description='Good working condition')),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_product(self):
        """delete specific product"""
        _id = {"product_id": 1}
        response = self.store_manager.delete(self.path + '/products/{}'.format(_id['product_id']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', str(response.data))

    def test_put_update_product(self):
        """update product if the product_id exist"""
        response = self.store_manager.put(self.path + '/products/3', data=json.dumps(
            dict(title='Macbook pro', serial='Mpc54321', Description='Faulty')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_new_product(self):
        """create new product if the id doesn't exist"""
        response = self.store_manager.put(self.path + '/products/6',
                                     data=json.dumps(dict(title='Macbook pro', serial='MCP12345', Description='Good working condition')),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_non_existing_product(self):
        """return status code 404 (when product not found)"""
        _id = {"product_id": 233}
        response = self.store_manager.get(self.path + '/products/{}'.format(_id['product_id']))
        self.assertEqual(response.status_code, 404)

    def test_get_product_missing_id(self):
        """reject request looking for a product but lacking an productID"""
        _id = {"product_id": None}
        response = self.store_manager.get(self.path + '/products/{}'.format(_id['product_id']))
        self.assertEqual(response.status_code, 404)

    def test_get_product_non_integer_id(self):
        """reject request looking for a product but lacking numerical productID"""
        _id = {"product_id": 'home'}
        response = self.store_manager.get(self.path + '/products/{}'.format(_id['product_id']))
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)