from models.product import ProductModel
from flask import request
from flask_restful import Resource
import os

class Products(Resource):
    
    def get(self,id):
        """return all products by category

        Returns:
            dict: containing all products by category (US05)
        """
        products = ProductModel.find_category(id)
        if products:
            return {'products': [product.json() for product in products]}, 200
        return {'message': 'No products found'}, 404


class Product(Resource):
  
    def get(self,id):
        """return one product by id

        Returns:
            dict: containing one product by id (US06)
        """
        product = ProductModel.find_product(id)
        if product:
            return product.json(), 200
        else:            
            return {'message': 'No product found'}, 404


    def patch(self, id):
        """US13 Update a product

        """ 
        #werkt nog niet
        req = request.get_json()
        print("patch_product: ", req)
        return ProductModel.update_product(req, id)


    def delete(self, id):
        """return one product by id

        Returns:
            dict: containing one product by id (US06)
        """
        #nog if statement toevoegen
        return ProductModel.delete_product(id)


class Search(Resource):
        
    def get(self):
        """return all products that matches search query

        Returns:
            dict: that matches search query
        """
        searchItems = request.args.get('q')
        print("searchItems: ", searchItems)
        if searchItems is None:
            products = ProductModel.find_all()
            if products: 
                return {'products': [product.json() for product in products]}, 200
        if searchItems == "":
            return {'message': 'Vul een zoekterm in'}, 400
        if searchItems is not None:
            products = ProductModel.product_search(searchItems)
            amount = len(products)
            print(amount)
            if products:
                return {'products': [product.json() for product in products]}, 200
            elif amount:
                return amount
        return {'message': 'Geen producten gevonden met deze omschrijving'}, 404


class AddProduct(Resource):
    
    def post(self):
        """US12 Add a new product to the database
        
        """ 
        req = request.get_json()
        print("addProduct: ", req)
        return ProductModel.add_product(req)
