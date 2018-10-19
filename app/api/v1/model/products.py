from .verify import Verify


class Products(Verify):
    products = []
    def __init__(self, items):
        self.items = items


    def check_user_input(self):
        payload = self.is_product_payload(self.items)
        if payload is False:
            return {'result': 'Payload is invalid'}
        elif self.is_empty([self.items['name'], self.items['category']]) is True:
            return {'result': 'data set is empty'}, 406
        elif self.is_whitespace([self.items['name'], self.items['category']]) is True:
            return {'result': 'data set contains whitespace only'}
        elif self.items['quantity'] < 1:
            return{'result': 'Product quantity cannot be less than 1'}
        elif self.items['price'] < 1:
            return {'result': 'Price cannot be less than 1'}
        else:
            return 1


    def add_product(self):
        self.items['id'] = len(Products.products)
        Products.products.append(self.items)
        return {'result': 'Product added'}, 201


    @classmethod
    def get_all(cls):
        if len(Products.products) == 0:
            return {'result': 'No products found'}, 404
        else:
            return Products.products, 200


    @classmethod
    def get_one(cls, productId):
        if len(Products.products) == 0:
            return {'result': 'No product found'}
        else:
            return Products.products[productId]