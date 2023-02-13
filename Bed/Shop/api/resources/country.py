from models.country import CountryModel
from flask import request
from flask_restful import Resource
import os

class Countries(Resource):
    
    def get(self):
        """return all countries

        Returns:
            dict: containing all countries
        """ 
        countries = CountryModel.find_all()
        if countries:
            return {'countries': [country.json() for country in countries]}, 200
        return {'message': 'No countries found'}, 404


class AddCountry(Resource):
    
    def post(self):
        """return all users

        Returns:
            dict: containing all users (US08)
        """ 
        req = request.get_json()
        return CountryModel.add(req)