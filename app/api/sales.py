"""Get all sales in store Manager"""
from flask import Flask
from flask_restful import Resource, reqparse, Api
app = Flask(__name__)
api = Api(app)

# Store the sales in a list made of dictionaries thus forming json.
sales = [
    {
        'sales_id': 1,
        'title': 'Macbook pro',
        'serial': 'MCP12345',
        'cost':120000,
        'attendant': 'Eden Hazard'
    },
    {
        'sales_id': 2,
        'title': 'Macbook pro',
        'serial': 'MCP12345',
        'cost':120000,
        'attendant': 'James Bond'
    },
    {
        'sales_id': 3,
        'title': 'Macbook pro',
        'serial': 'MCP12345',
        'cost':120000,
        'attendant': 'wilfred katuka'
    }
]

"""Sale Entry resource parsed during the request"""


class Sale(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Content Missing"),
    parser.add_argument('serial', type=str, required=True, help="Content Serial Missing"),
    parser.add_argument('cost', type=str, required=True, help="Content cost Missing"),
    parser.add_argument('attendant', type=str, required=True, help="Content Description Missing.")

    """get a specific sale entry"""

    def get(self, sale_id):
        sale = next(filter(lambda x: x['sale_id'] == sale_id, sales), None)
        return {'sale': sale}, 200 if sale else 404

    """modify a sale entry"""

    def put(self, sale_id):
        data = Sale.parser.parse_args()

        sale = next(
            filter(lambda x: x['sale_id'] == sale_id, sales), None)
        if sale is None:
            return 'sale not found', 404
        else:
            sale = {'sale_id': sale_id,
                     'title': data['title'],
	             'serial': data['serial'],
                    'cost': data['cost'],
                     'attendant': data['attendant']}
            sale.update(data)
        return sale, 200

    """delete a sale entry from store manager"""

    def delete(self, sale_id):
        global sales
        sales = list(filter(lambda x: x['sale_id'] != sale_id, sales))
        return {'message': 'sale successfully deleted'}


class Sales(Resource):
    """return all sales"""

    def get(self):
        return {'sales': sales}

    """post a new sale entry"""

    def post(self):
        data = Sale.parser.parse_args()

        sale = {'sale_id': 12, 'title': data['title'], 'serial': data['serial'],'cost': 120000, 'attendant': data['attendant']}
        sales.append(sale)
        return sale, 201


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
        {'Endpoints': '/api/v1/sales'}]
        """


api.add_resource(Sale, '/api/v1/sales/<int:sale_id>')
api.add_resource(Sales, '/api/v1/sales')

if __name__ == '__main__':
    app.run(port=5000, debug=True)