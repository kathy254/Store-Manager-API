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


    def test_payload_is_invalid(self):
        payload = {'productId':0,'quantity':10,'xyz':''} 
        response = self.test.post('/sales/',content_type=self.content_type, data=json.dumps(payload))
        data = json.loads(response.get_data().decode('UTF-8'))
        self.assertEqual(response.status_code,406)
        self.assertEqual(data,{'result':'Payload is invalid'})


    def test_minimum_quantity(self):
		payload = {'productId':0,'quantity':-10}
		response = self.test.post('/sales/',content_type=self.content_type, data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'Product quantity cannot be less than 1'})


    def test_data_is_invalid(self):
		payload = {'productId':0,'quantity':'0'}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,400)
		self.assertEqual(data['message'],'Input payload validation failed')


    def test_minimum_id(self):
		payload = {'productId':-2,'quantity':90}
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(payload))
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result':'productId can not be less than 0'})


class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		self.product = {'name': 'Gucci dress', 'quantity': 1, 'category': "Girls' dresses", 'moq':0, 'price':100}
		self.test.post('/products/',content_type=self.content_type,
			data=json.dumps(self.product))
		self.payload = {'quantity':10,'productId':0}

	
	def test_add_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,201)


	def test_get_all_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,405)
		response = self.test.get('/sales/',content_type=self.content_type)
		data = json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(data.status_code,200)


	def get_one_sales(self):
		response = self.test.post('/sales/',content_type=self.content_type,
			data=json.dumps(self.payload))
		self.assertEqual(response.status_code,201)
		response = self.test.get('/sales/{}'.format(0),content_type=self.content_type)
		self.assertEqual(response.status_code,200)
