from flask import request
from flask_restplus import Namespace, Resource, fields


from ..model.sales import Sales
from ..model.products import Products
from ..utilities.auth import get_token


store_sales = Namespace('sales', description='Sales Endpoints')


mod = store_sales.model('sales model', {
    'productId': fields.Integer(description='Name of product sold'),
	'quantity': fields.Integer(description='Quantity of product sold'),
    'price': fields.Integer(description='Price of product sold')
})


@store_sales.route('')
class GetAll(Resource):


    @get_token
    @store_sales.doc(security='apikey')
    def get(self):
        sales = len(Sales.sales)
        if sales < 1:
            return {'result': 'No sales found'}, 404
        else:
            return Sales.sales, 200


    @store_sales.expect(mod, validate=True)
    @get_token
    @store_sales.doc(security='apikey')
    def post(self):
        data=request.get_json()
        obj = Sales(data)
        data['price'] = 0
        if obj.check_sales_input() == 1:
            try:
                return obj.add_sales_record()
            except IndexError:
                return{'result': 'Product ID is invalid'}, 406
            except KeyError:
                return {'result': 'Product ID is invalid'}, 406
        else:
            return obj.check_sales_input()
            

@store_sales.route('/<saleId>')
class GetSingle(Resource):

    @get_token
    @store_sales.doc(security='apikey')
    def get(self, saleId):
        try:
            return Sales.sales[int(saleId)]
        except IndexError:
            return {'result': 'Sale does not exist'}