from .verify import Verify


class Sales(Verify):
	sales = []
	def __init__(self,items):
		self.items = items

	def check_user_input(self):
		if self.is_sales_payload(self.items) is False:
			return {'result': 'Payload is invalid'},406
		elif self.items['quantity'] < 1:
			return {'result': 'Product quantity can not be less than 1'},406
		elif self.items['productId'] < 0:
			return {'result': 'productId can not be less than 0'},406
		else:
			return 1