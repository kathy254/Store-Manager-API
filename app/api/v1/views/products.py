from flask import request
from flask_restplus import Namespace, Resource, fields


from ..utilities.auth import get_token
from ..model.products import Products


store_product = Namespace('products', description='Products Endpoint')

mod = store_product.model('product model', {
    'name': fields.String(description='Product name'),
    'quantity': fields.Integer(descirption='Product Quantity'),
    'moq': fields.Integer(description='Minimum Inventory Quantity'),
    'category': fields.String(description='Product category'),
    'price': fields.Integer(description='Price of product'),
})


@store_product.route('')
class AllProducts(Resource):


    @get_token
    @store_product.doc(security='apikey')
    def get(self):
        return Products.get_all_products()


    @store_product.expect(mod, validate=True)
    # @get_token
    @store_product.doc(security='apikey')
    def post(self):
        data = request.get_json()
        obj = Products(data)
        if obj.check_product_input() == 1:
            return obj.add_product()
        else:
            return obj.check_product_input()


@store_product.route('/<productId>')
class SingleProduct(Resource):


    @get_token
    @store_product.doc(secret='apikey')
    def get(self, productId):
        try:
            return Products.get_product_by_id(int(productId))
        except IndexError:
            return {'result': 'No products found'}, 404


