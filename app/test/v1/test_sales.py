import unittest
import json

from ... import create_app
from ...api.v1.model.sales import Sales

class TestInvalidData(unittest.TestCase):
	
    
    
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'

	def tearDown(self):
		self.test = None
		self.content_type = None


	#This class tests for invalid json payload
	def test_invalid_payload(self):
		payload = {'productId':0,'quantity':10,'abc':''}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'Payload is invalid'})


	#This tests for invalid data types
	def test_invalid_data_type(self):
		payload = {'productId':0,'quantity':'0'}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,400)
		self.assertEqual(data['message'],'Input payload validation failed')


	#Test for when a user enters a quantity of less than 1
	def test_min_quantity(self):
		payload = {'productId':0,'quantity':-4}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'Product quantity can not be less than 1'})


	#Test for when user enters an id that's less than 1
	def test_min_id(self):
		payload = {'productId':-2,'quantity':10}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'productId can not be less than zero'})


	#Test for a product ID that's out of range
	def test_max_id(self):
		payload = {'productId':10000,'quantity':1}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'invalid product id'})


class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		self.product = {'name': 'Gucci dress', 'quantity': 1, 'category': 'dresses','moq':0,'price':100}
		self.test.post('/products/',content_type=self.content_type,
			data=json.dumps(self.product))
		self.payload = {'quantity':10,'productId':0}


	def tearDown(self):
		self.test = None
		self.content_type = None
		self.product = None
		self.payload = None
		

	def test_add_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,201)


	def test_get_all_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,201)
		response = self.test.get('/sales/',content_type=self.content_type)
		self.assertEqual(response.status_code,200)


	def get_one_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,201)
		response = self.test.get('/sales/{}'.format(0),content_type=self.content_type)
		self.assertEqual(response.status_code,200)


if __name__ == '__main__':
	unittest.main()