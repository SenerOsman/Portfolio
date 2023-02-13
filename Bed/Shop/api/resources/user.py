from models.user import UserModel
from flask import request
from flask_restful import Resource
import os
import re 
from flask_jwt import JWT, jwt_required, current_identity

class Users(Resource):
    
    def post(self):
        """return newly added user details

        Returns:
            dict: containing user data (US08)
        """ 
        req = request.get_json()
        return UserModel.register(req)

 
class Load_user(Resource):
    @jwt_required()
    def get(self):
        """Login user

        Returns:
            dict: containing logged in user (US09)
        """
        currentUser = current_identity.json()
        print("user: ", currentUser)
        return currentUser


class All_users(Resource):
    @jwt_required()
    def get(self):
        """return all users

        Returns:
            dict: containing all users
        """
        users = UserModel.find_all()
        if users:
            return {'users': [user.json() for user in users]}, 200
        return {'message': 'No users found'}, 404


class Update_user(Resource):    

    def patch(self, id):
        """return newly added user details

        Returns:
            dict: containing user data (US08)
        """ 
        req = request.get_json()
        return UserModel.update(req, id)


    def delete(self, id):
        """return one user by id

        Returns:
            dict: containing one user by id 
        """
        return UserModel.delete(id)