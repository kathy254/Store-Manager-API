import unittest
import json 

from passlib.hash import pbkdf2_sha256 as sha256

from ... import create_app
from ...api.v1.model.users import Accounts

class TestInvalidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'


	def tearDown(self):
		self.test = None
		self.content_type = None


	
	def test_incorrect_role(self):
		payload = {'role': 'not role', 'password': 'admin', 'email_address': 'string@gmail.com'}
		response = self.test.post('api/v1/auth/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result': 'Role is invalid'})
        

	def test_invalid_login(self):
		payload = {'role': 'admin', 'password': 'notpassword', 'email_address': 'not@gmail.com'}
		response = self.test.post('api/v1/auth/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result': 'email or password invalid'})

class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'role': 'admin', 'password': 'admin', 'email_address': 'admin@gmail.com'}
		response = self.test.post('api/v1/auth/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'X-API-KEY':'{}'.format(token)}


	def tearDown(self):
		self.test = None
		self.content_type = None


	def test_registered_user_login(self):
		resp_register = self.test.post(
			'/api/v1/auth/register',
			data = json.dumps(dict(
				email_address = 'kama@gmail.com',
				password = 'abcd'
			)),
			content_type='application.json',
		)

		data_register = json.loads(resp_register.data.decode())
		self.assertTrue(data_register['status'] == 'success')
		self.assertTrue(data_register['message'] == 'Account created. Please log in')
		self.assertTrue(data_register['token'])
		self.assertTrue(resp_register.content_type == 'application/json')
		self.assertEqual(resp_register.status_code, 201)

		#login for registered user

		response = self.test.post(
			'/api/v1/auth/login',
			data=json.dumps(dict(
				email_address = 'kama@gmail.com',
				password = 'abcd'
			)),
			content_type='application/json'
		)

		data = json.loads(response.data.decode())
		self.assertTrue(data['status'] == 'ok')
		self.assertTrue(data['message'] == 'You have successfully logged in')
		self.assertTrue(data['token'])
		self.assertTrue(response.content_type == 'application/json')
		self.assertTrue(response.status_code, 200)
		

	def test_register_attendant(self):
		payload = {'role': 'admin', 'last_name': 'string', 'password': 'abcd', 'email_address': 'string@gmail.com',
		 'first_name': 'string'}
		response = self.test.post('api/v1/auth/register',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,200)

if __name__ == '__main__':
	unittest.main()