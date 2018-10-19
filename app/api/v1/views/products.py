from flask import request
from flask_restplus import Namespace, Resource, fields


from ..model.products import Products


store_product = Namespace('products', description='Products Endpoint')

mod = store_product.model('product model', {
    'name': fields.String(description='Product name'),
    'quantity': fields.Integer(descirption='Product Quantity'),
    'moq': fields.Integer(description='Minimum Inventory Quantity'),
    'category': fields.String(description='Product category'),
    'price': fields.Integer(description='Price of product'),
})


@store_product.route('/')
class AllProducts(Resource):


    def get(self):
        return Products.get_all()


    @store_product.expect(mod, validate=True)
    def post(self):
        data = request.get_json()
        obj = Products(data)
        if obj.check_user_input() == 1:
            return obj.add_product()
        else:
            return obj.check_user_input()


@store_product.route('/<productId>')
class SingleProduct(Resource):
    
    def get(self, productId):
        try:
            return Products.get_one(int(productId))
        except IndexError:
            return {'result': 'No products found'}, 404


