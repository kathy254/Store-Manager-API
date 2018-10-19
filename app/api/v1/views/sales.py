from flask import request
from flask_restplus import Namespace, Resource, fields


from ..model.sales import Sales
from ..model.products import Products


store_sales = Namespace('sales', description='Sales Endpoints')


mod = store_sales.model('sales model', {
    'productId': fields.Integer(description='Name of product sold'),
	'quantity': fields.Integer(description='Quantity of product sold')
})

@store_sales.route('/')
class GetAll(Resource):


    def get(self):
        sales = len(Sales.sales)
        if sales < 1:
            return {'result': 'No sales found'}, 404
        else:
            return Sales.sales, 200


@store_sales.expect(mod, validate=True)
def post(self):
    try:
        data=request.get_json()
        obj = Sales(data)
        data['price'] = 0
        if obj.user_input() == 1:
            prodId = Products.get_one(data['productId'])
            total = prodId[data['productId']]['price']*data['quantity']
            data['price'] = total
            Sales.sales.append(data)
            return {'result': 'Sale added'}, 201
        else:
            return obj.user_input()
    except IndexError:
        return {'result': 'Product Id is invalid'}, 406


@store_sales.route('/<saleId>')
class GetSingle(Resource):
    def get(self, saleId):
        try:
            return Sales.sales[int(saleId)]
        except IndexError:
            return {'result': 'Sale does not exist'}