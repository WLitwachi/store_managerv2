"""Get all products in store Manager"""
from flask import Flask
from flask_restful import Resource, reqparse, Api
from app.api.decorator import is_logged_in

app = Flask(__name__)
api = Api(app)

# Store the products in a list made of dictionaries thus forming json.
products = [
    {
        'product_id': 1,
        'title': 'Macbook pro',
        'serial': 'MCP12345',      
        'description': 'Good working condition'
    },
    {
        'product_id': 2,
        'title': 'Macbook pro',
        'serial': 'MCP12345',      
        'description': 'Good working condition'
    },
    {
        'product_id': 3,
        'title': 'Macbook pro',
        'serial': 'MCP12345',      
        'description': 'Good working condition'
    }
]

"""Product Entry resource parsed during the request"""


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Content Missing"),
    parser.add_argument('serial', type=str, required=True, help="Content Serial Missing"),
    parser.add_argument('description', type=str, required=True, help="Content description Missing.")

    """get a specific product entry"""

    def get(self, product_id):
        product = next(filter(lambda x: x['product_id'] == product_id, products), None)
        return {'product': product}, 200 if product else 404

    """modify a product entry"""


    def put(self, product_id):
        data = Product.parser.parse_args()

        product = next(
            filter(lambda x: x['product_id'] == product_id, products), None)
        if product is None:
            return 'product not found', 404
        else:
            product = {'product_id': product_id,
                     'title': data['title'],
	                 'serial': data['serial'],
                     'description': data['description']}
            product.update(data)
        return product, 200

    """delete a product entry from store manager"""

    @is_logged_in
    def delete(self, product_id):
        global products
        products = list(filter(lambda x: x['product_id'] != product_id, products))
        return {'message': 'Product successfully deleted'}


class Products(Resource):
    """return all products"""

    def get(self):
        return {'products': products}

    """post a new product entry"""


    def post(self):
        data = Product.parser.parse_args()

        product = {'product_id': 12, 'title': data['title'], 'serial': data['serial'], 'description': data['description']}
        products.append(product)
        return product, 201


# root : GET /
'''Return details about the api server'''


@app.route('/')
def root():
    return """ [
        {'AppName': 'StoreManager'},
        {'Version': 1},
        {'Author': 'katuka Litwachi'},
        {'Email' : 'katuka.wilfred8@gmail.com'},
        {'host' : 'localhost or github.com or heroku'},
        {'Endpoints': '/api/v1/products'}]
        """


api.add_resource(Product, '/api/v1/products/<int:product_id>')
api.add_resource(Products, '/api/v1/products')

if __name__ == '__main__':
    app.run(port=5000, debug=True)