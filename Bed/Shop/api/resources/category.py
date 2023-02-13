from models.category import CategoryModel
from flask import request
from flask_restful import Resource
import os

class Categories(Resource):
    
    def get(self):
        """return all categories

        Returns:
            dict: containing all categories
        """
        categories = CategoryModel.find_all()
        if categories:
            return {'categories': [category.json() for category in categories]}, 200
        return {'message': 'No categories found'}, 404


class AddCategory(Resource):

    def post(self):
        """US15 Add a category
        
        """ 
        req = request.get_json()
        print("categorie: ", req)
        return CategoryModel.addCategory(req)


class Update_category(Resource):

    def get(self,id):
        """return one product by id

        Returns:
            dict: containing one product by id 
        """
        category = CategoryModel.find(id)
        if category:
            return category.json(), 200
        else:            
            return {'message': 'No category found'}, 404


    def patch(self, id):
        """US13 Update a product

        """ 
        #werkt nog niet
        req = request.get_json()
        print("patch_product: ", req)
        return CategoryModel.update_cat(req, id)

        
    def delete(self, id):
        """return one product by id

        Returns:
            dict: containing one product by id (US06)
        """
        return CategoryModel.delete(id)