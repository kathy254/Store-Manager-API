import jwt
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

from instance.config import secret_key
from .verify import Verify

userId = 1
	
user_list = []

class Accounts(Verify):	

	

	def __init__(self, first_name, last_name, email_address, password, role):
		self.first_name = first_name
		self.last_name = last_name
		self.email_address = email_address
		self.password=password
		self.role = role

	def create_new_user(self):
		new_user = dict(
            first_name=self.first_name,
			last_name=self.last_name,
			email_address=self.email_address,
			password=self.password,
			role= self.role
		)
		user_list.append(new_user)
		return new_user	


	@staticmethod
	def get_one_user(email_address):
		one_user= [user for user in user_list if user['email_address'] == email_address]

		if one_user:
			return one_user[0]
		return 'User not found'

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
		return sha256.verify(password, hash)
			


	@staticmethod
	def encode_login_token(email_address, role):
		try:
			payload = {
				'exp': datetime.datetime.now() + datetime.timedelta(hours=24),
				'iat': datetime.datetime.now(),
				'sub': email_address,
				'role': role
			}

			token = jwt.encode(
				payload,
				secret_key,
				algorithm='HS256'
			)

			return token

		except Exception as e:
			return e

	@staticmethod
	def decode_auth_token(token):
		"""Method to decode the auth token"""

		try:
			payload = jwt.decode(token, secret_key, options={'verify_iat': False})
			return payload
		except jwt.ExpiredSignatureError:
			return {'message': 'Signature expired. Please log in again.'}
		except jwt.InvalidTokenError:
			return {'message': 'Invalid token. Please log in again.'}
		
