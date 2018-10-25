from flask import Blueprint
from flask_restplus import Api


from .views.products import store_product
from .views.sales import store_sales
from .views.users import store_users

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


app_v1 = Blueprint('app_v1',__name__, url_prefix='/api/v1')
api_v1 = Api(app_v1, title='Store Manager', version='1.0', description='Store Manager api v1', authorizations=authorizations)


api_v1.add_namespace(store_product)
api_v1.add_namespace(store_sales)
api_v1.add_namespace(store_users)
