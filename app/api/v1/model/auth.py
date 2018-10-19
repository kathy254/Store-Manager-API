from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User:

    users = []

    def __init__(self, email, password):
        #initialize all uses with an email and a password
        self.email = email
        self.password = password
    

    def password_is_valid(self, password):
        
        #Check the password against its hash to validate the user's password

        return Bcrypt().check_password_hash(self.password, password)

    
    def generate_token(self, user_id):

        #Generates the access token to be used as the authorizati

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=2),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

   
    @staticmethod
    def decode_token(token):
        #Decode the access token from the authorization header.
       
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"