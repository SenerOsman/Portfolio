import os
from flask import Flask, send_from_directory
from flask_restful import Api
#from resources import *
from resources.category import Categories, AddCategory, Update_category
from resources.product import Products, Product, Search, AddProduct
from resources.country import Countries, AddCountry
from resources.user import Users, All_users, Load_user, Update_user
from resources.userrole import Userrole
from resources.order import Orders, showOrders, updateOrder
from auth import identity, authenticate
from flask_jwt import JWT

# ============================================================================================
# =================================================================== INITIALIZATION =========
# ============================================================================================

# Create a new Flask application
app = Flask(__name__)
# Add a secret key. Important for hashing (e.g. with login handling)
app.secret_key = os.getenv('SECRET')
# Create a new API
api = Api(app, prefix=os.getenv('API_PREFIX'))
app.config['JWT_AUTH_URL_RULE'] = os.getenv('API_PREFIX') + '/auth'
jwt = JWT(app, authenticate, identity)

# ============================================================================================
# =============================================================== FRONTEND REDIRECTS =========
# ============================================================================================

@app.route('/')
def index():
    """Redirects the base url '/' to the webshop/index.html file

    Returns:
        string: file content
    """
    return send_from_directory('../webshop', 'index.html')

@app.route('/<path:path>')
def shop(path):
    """Redirects all requests to the front end (webshop)

    Args:
        path (path): path to requested file

    Returns:
        string: file content
    """
    return send_from_directory('../webshop', path)
    
# ============================================================================================
# =================================================================== ERROR HANDLING =========
# ============================================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Returns a JSON on 404
    
    Returns:
        object: error message
    """
    return {'message': 'resource not found'}, 404
    
# ============================================================================================
# ======================================================================== ENDPOINTS =========
# ============================================================================================

api.add_resource(Categories, '/categories/') #us04
api.add_resource(AddCategory, '/categories') #us15
api.add_resource(Update_category, '/categories/<id>')
api.add_resource(Products, '/categories/<id>/products') #us05
api.add_resource(Product, '/products/<id>') #us06
api.add_resource(Search, '/products/') #us07
api.add_resource(AddProduct, '/products') #us12
api.add_resource(Countries, '/countries/') #us08 & us16
api.add_resource(AddCountry, '/countries') #us17
api.add_resource(Users, '/users') #us08
api.add_resource(All_users, '/users') 
api.add_resource(Load_user, '/users/me') #us09
api.add_resource(Update_user, '/users/<id>') #us16
api.add_resource(Userrole, '/userroles') #us08
api.add_resource(Orders, '/orders') #us10
api.add_resource(updateOrder, '/orders/<id>') #us19
api.add_resource(showOrders, '/users/<id>/orders') #us10 & 19


# ============================================================================================
# ================================================================ START APPLICATION =========
# ============================================================================================

if __name__ == '__main__':
    app.run(debug=True)