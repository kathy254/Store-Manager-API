from flask import Flask, request, jsonify, Blueprint, json, make_response
from flask_restplus import Resource, reqparse, Namespace, fields, Api

from ..utilities.auth import get_token
from ..model.users import Accounts


parser=reqparse.RequestParser()
parser.add_argument('first_name', help='This field cannot be blank')
parser.add_argument('last_name', help='This field cannot be blank')
parser.add_argument('email_address', help='This field cannot be blank')
parser.add_argument('role', help='This field cannot be blank')
parser.add_argument('password', help='This field cannot be blank')


store_users = Namespace('auth', description='Users endpoints')
mod_register = store_users.model('register store attendant',{
	'first_name':fields.String('attendant\'s first name'),
	'last_name': fields.String('attendants\'s last name'),
	'email_address': fields.String('attendant\'s email'),
	'role': fields.String('attendant\'s role'),
	'password': fields.String('attendant\'s password')
	})


@store_users.route('/register')
class RegisterStoreAttendant(Resource):
	@store_users.doc(security='apikey')
	@store_users.expect(mod_register)
	def post(self):
		args = parser.parse_args()
		first_name = args['first_name']
		last_name = args['last_name']
		email_address = args['email_address']
		password = args['password']
		role = args['role']


		email_found = Accounts.get_one_user(email_address)
		
		if email_found == 'User not found':

			try:
				create_user = Accounts(first_name, last_name, email_address, Accounts.generate_hash(password), role)
				new_user = create_user.create_new_user()
				return make_response(jsonify({
					'status': 'success',
					'message': 'Account created. Please log in',
					'users': new_user
				}), 201)

			except Exception as e:
				return make_response(jsonify({
					'message': str(e),
					'status': 'failed'
				}), 500)

		return make_response(jsonify({
			'status': 'failed',
			'message': 'Email address already exists. Please log in.'
		}), 500)


mod_login = store_users.model('users model',{
	'email_address':fields.String('Email address'),
	'password':fields.String('Password')
	})

@store_users.route('/login')
class Login(Resource):
	@store_users.expect(mod_login)
	def post(self):
		args = parser.parse_args()
		email_address=args['email_address']
		password=args['password']

		try:
			present_user = Accounts.get_one_user(email_address)
			if present_user == 'User not found':
				return make_response(jsonify({
					'status': 'failed',
					'message': 'User does not exist'
				}), 200)



			if present_user and Accounts.verify_hash(password, present_user['password']):
				print("user exists")
				role = present_user['role']
				email_address=present_user['email_address']
				token = Accounts.encode_login_token(email_address, role)

				if token:
					return make_response(jsonify({
						'status': 'ok',
						'message': 'You have successfully logged in',
						'token': token.decode()
					}), 200)

			else:
				return make_response(jsonify({
					'status': 'failed',
					'message': "Email address or password is incorrect"
				}), 400)

		except Exception as e:
			return make_response(jsonify({
				'message': str(e),
				'status': 'failed'
			}), 500)

		
