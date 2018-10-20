import unittest
import json

from ... import create_app


class TestInvalidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'


	def tearDown(self):
		self.test = None
		self.content_type = None


	def test_invalid_email(self):
		payload = {'role': 'admin', 'password': 'abcd', 'email address': 'stringgmail.com'}
		response = self.test.post('/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result': 'Email address is invalid'})


	def test_incorrect_role(self):
		payload = {'role': 'not role', 'password': 'admin', 'email address': 'string@gmail.com'}
		response = self.test.post('/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result': 'Role is invalid'})
        

	def test_invalid_login(self):
		payload = {'role': 'admin', 'password': 'notpassword', 'email address': 'not@gmail.com'}
		response = self.test.post('/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,406)
		self.assertEqual(data,{'result': 'email or password invalid'})

class TestValidData(unittest.TestCase):
	def setUp(self):
		self.test = create_app('testing').test_client()
		self.content_type = 'application/json'
		payload = {'role': 'admin', 'password': 'admin', 'email address': 'admin@gmail.com'}
		response = self.test.post('/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		token = data['result']
		self.headers = {'X-API-KEY':'{}'.format(token)}


	def tearDown(self):
		self.test = None
		self.content_type = None


	def test_user_login(self):
		payload = {'role': 'admin', 'password': 'abcd', 'email address': 'admin@gmail.com'}
		response = self.test.post('/users/login',content_type=self.content_type,
			data=json.dumps(payload))
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,200)


	def test_register_attendant(self):
		payload = {'role': 'admin', 'last_name': 'string', 'password': 'abcd', 'email address': 'string@gmail.com',
		 'first_name': 'string'}
		response = self.test.post('/users/register',content_type=self.content_type,
			data=json.dumps(payload),headers=self.headers)
		data =json.loads(response.get_data().decode('UTF-8'))
		self.assertEqual(response.status_code,200)

if __name__ == '__main__':
	unittest.main()