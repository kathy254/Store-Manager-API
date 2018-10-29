import unittest
import json

from ... import create_app
from ...api.v1.model.sales import Sales

class TestInvalidData(unittest.TestCase):
	
    
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'password': 'admin', 'email_address': 'admin@gmail.com'}
		response = self.test.post('api/v1/auth/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'Authorization':'{}'.format(token)}


	def tearDown(self):
		self.test = None
		self.content_type = None


	#test if the user entered a valid json payload
	def test_invalid_payload(self):
		payload = {'Product_name':'Gucci dress','productId':0,'quantity':10,'xyz':''}
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'Payload is invalid'})


	#test if user entered a valid data type
	def test_invalid_data_type(self):
		payload = {'Product_name': 'Gucci dress', 'productId':0,'quantity':'0', 'price': 100}
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,400)
		self.assertEqual(data['message'],'Input payload validation failed')


	#test if the quantity is less than 1
	def test_min_quantity(self):
		payload = {'Product_name': 'Gucci dress', 'productId':0,'quantity':-5, 'price': 100}
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'Product quantity cannot be less than 1'})


	#test if the product ID is less than 0
	def test_minimum_id(self):
		payload = {'Product_name': 'Gucci dress', 'productId':-2,'quantity':90, 'price': 100}
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data, {'result':'productId cannot be less than 0'})

	
class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'role': 'admin', 'password': 'admin', 'email': 'admin@gmail.com'}
		response = self.test.post('api/v1/auth/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'Authorization':'{}'.format(token)}
		self.product = {'name': 'Gucci dress', 'quantity': 21, 'category': 'dresses','moq':0,'price':100}
		self.test.post('api/v1/products/',content_type=self.content_type,
			data=json.dumps(self.product),headers=self.headers)
		self.payload = {'quantity':10,'productId':0}


	def tearDown(self):
		self.test = None
		self.content_type = None
		self.product = None
		self.payload = None


	def get_one_sales(self):
		
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		self.assertEqual(response.status_code,200)
		response = self.test.get('api/v1/sales/{}'.format(0),content_type=self.content_type)
		self.assertEqual(response.status_code,200)


	def test_add_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(data,{'result': 'sales added'})
		self.assertEqual(response.status_code,201)


	def test_get_all_sales(self):
		response = self.test.post('api/v1/sales/',content_type=self.content_type,
			data=json.dumps(self.payload),headers=self.headers)
		self.assertEqual(response.status_code,201)
		response = self.test.get('api/v1/sales/',content_type=self.content_type
			,headers=self.headers)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,200)


if __name__ == '__main__':
	unittest.main()