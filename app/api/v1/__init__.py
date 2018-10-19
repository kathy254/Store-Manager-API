from flask import Blueprint
from flask_restplus import Api


from .views.products import store_product
from .views.sales import store_sales


app_v1 = Blueprint('app_v1',__name__)
api_v1 = Api(app_v1, title='Store Manager', version='1.0', description='Store Manager api v1')


api_v1.add_namespace(store_product)
api_v1.add_namespace(store_sales)
