from flask import request
import os
import sqlite3
from models.product import ProductModel


class OrderLineModel:
    
    def __init__(self, id, product, order, amount, total_price):
        """OrderLineModel constructor

        Args:
            id (int): database id
            product (int): product id
            order (int): order id
            amount (int):
            total_price (int): in cents
        """
        self.id = id
        self.product = product
        self.order = order
        self.amount = amount
        self.total_price = total_price


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        self_dict=self.__dict__
        product = ProductModel.find_product(self.product)
        self_dict["product"] = product.json()
        return self_dict