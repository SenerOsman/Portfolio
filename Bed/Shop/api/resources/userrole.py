from models.userrole import UserroleModel
from flask import request
from flask_restful import Resource
import os

class Userrole(Resource):
    
    def get(self):
        """return all userroles

        Returns:
            dict: containing all userroles
        """ 
        userroles = UserroleModel.find_all()
        if userroles:
            return {'userroles': [userrole.json() for userrole in userroles]}, 200
        return {'message': 'No userroles found'}, 404