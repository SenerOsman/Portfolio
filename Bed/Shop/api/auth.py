import os
import sqlite3
from werkzeug.security import safe_str_cmp
from models.user import UserModel, UserModel2
from flask_jwt import JWT, jwt_required, current_identity
import json
from models.userrole import UserroleModel


def authenticate(email, password):
    """Creates a Token by checking the email and password

    Args:
        email ([type]): [description]
        password ([type]): [description]

    Returns:
        Valid JWT
    """    
    user = UserModel.login(email, password)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    """If authentication is validated, user details will be returned

    Args:
        payload ([type]): Username/password

    Returns:
        [type]: user details
    """    
    con = sqlite3.connect("db/webshop.db")
    cur = con.cursor()
    user_id = "%s" % payload['identity']
    print("user inlog successfull")
    for row in cur.execute("SELECT * FROM users WHERE id =" + user_id):
        user = UserModel2(row[0], row[10], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[12], row[13], row[9])
        return user


#bron: https://pythonhosted.org/Flask-JWT/