from .verify import Verify


class Products(Verify):
	products = []
	def __init__(self,items):
		self.items = items


	def check_product_input(self):
		payload=self.is_product_payload(self.items)
		strings = [self.items['name'], self.items['category']]
		if payload is False:
			return {'result':'Payload is invalid'},406
		elif self.is_empty(strings) is True:
			return {'result':'Data set is empty'},406
		elif self.is_whitespace(strings) is True:
			return {'result':'data set contains only white space'},406
		elif self.items['quantity'] < 1:
			return {'result':'Product quantity cannot be less than 1'},406
		elif self.items['price'] < 1:
			return {'result':'Price cannot be less than 0'},406
		else:
			return 1

	def add_product(self):
		self.items['id'] = len(Products.products)
		Products.products.append(self.items)
		return {'result': 'product added'},201

	@classmethod
	def get_all_products(cls):
		if len(Products.products) == 0:
			return {'result': 'No products found'},404
		else:
			return Products.products, 200

	@classmethod
	def get_product_by_id(cls,productId):
		if len(Products.products) == 0:
			return {'result': 'No products found'},404
		else:
			return Products.products[productId],200