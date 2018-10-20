from flask import request
from flask_restplus import Resource, Namespace,fields

from ..utilities.auth import get_token
from ..model.users import Accounts

store_users = Namespace('users',description='Users endpoints')
mod_login = store_users.model('users model',{
	'email':fields.String('Email address'),
	'role': fields.String('Roles'),
	'password':fields.String('Password')
	})

mod_register = store_users.model('register store attendant',{
	'first_name':fields.String('attendant\'s first name'),
	'last_name': fields.String('attendants\'s last name'),
	'email address': fields.String('attendant\'s email'),
	'role': fields.String('attendant\'s role'),
	'password': fields.String('attendant\'s role')
	})

@store_users.route('/login')
class Login(Resource):
	@store_users.expect(mod_login)
	def post(self):
		obj = Accounts(request.get_json())
		if obj.check_user_input() == 1:
			return obj.login()
		else:
			return obj.check_user_input()


@store_users.route('/register')
class RegisterStoreAttendant(Resource):
	@get_token
	@store_users.doc(security='apikey')
	@store_users.expect(mod_register)
	def post(self):
		data = request.get_json()
		obj = Accounts(data)
		if obj.check_register_input() == 1:
			return Accounts.accounts
		else:
			return obj.check_register_input()