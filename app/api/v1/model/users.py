import jwt

from .verify import Verify


class Accounts(Verify):
	

	accounts = [{'first_name': 'admin', 'last_name': 'admin', 
	'email address': 'admin@gmail.com','password': 'admin'}]
	def __init__(self,items):
		self.items = items
		self.role = self.items['role'] != 'admin' and self.items['role'] != 'attendant'


	def check_user_input(self):
		strings = [self.items['email address'],self.items['role'],self.items['password']]
		payload=self.is_login_payload(self.items) 
		if payload is False:
			res = {'result':'Payload is invalid'},406
		elif self.is_empty(strings) is True:
			res = {'result': 'data set is empty'},406
		elif self.is_whitespace(strings) is True:
			res = {'result': 'data set contains only white spaces'},406
		elif self.is_email(self.items['email address']) is True:
			res = {'result': 'Email address is invalid'}, 406
		elif self.role:
			res = {'result': 'Role is invalid'}, 406
		else:
			res = 1
		return res

	def login(self):
		token = jwt.encode({'email address':self.items['email address'],'role':self.items['role']},'765uytjhgmnb',
			algorithm='HS256').decode('UTF-8')
		for account in Accounts.accounts:
			if account.get('email address') == self.items['email address']:
				return {'result':token}
		return {'result': 'email or password invalid'},406

	def check_register_input(self):
		strings = [self.items['first_name'],self.items['last_name'],self.items['role'],
		self.items['email address'],self.items['password']]
		payload = self.is_register_payload(self.items)
		if payload is False:
			return {'result':'Payload is invalid'},406
		elif self.is_whitespace(strings) is True:
			return {'result': 'data set contains only white spaces'},406
		elif self.is_email(self.items['email address']) is True:
			return {'result': 'Email address is invalid'}, 406
		elif self.role:
			return {'result': 'Role is invalid'}, 406
		else:
			Accounts.accounts.append(self.items)
			return 1
