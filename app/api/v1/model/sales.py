from .verify import Verify
from .products import Products


class Sales(Verify):
	sales = []
	def __init__(self,items):
		self.items = items

	def check_sales_input(self):
		if self.is_sales_payload(self.items) is False:
			return {'result': 'Payload is invalid'},406
		elif self.items['quantity'] < 1:
			return {'result':'Product quantity cannot be less than 1'},406
		elif self.items['productId'] < 0:
			return {'result':'productId cannot be less than 0'},406
		else:
			return 1

	def add_sales_record(self):
		items = self.items
		prodID = Products.get_product_by_id(items['productId'])
		total = prodID[items['productId']]['price'] * items['quantity']
		items['price'] = total
		Sales.sales.append(items)
		return {'result': 'sales added'}, 201