from models.order import OrderModel
from flask import request
from flask_restful import Resource
import os
from auth import authenticate, identity
from models.order_line import OrderLineModel
from flask_jwt import JWT, jwt_required, current_identity
import json


class Orders(Resource):
    
    def get(self):
        """return all orders [US19]

        Returns:
            dict: containing all 
        """
        orders = OrderModel.find_all()
        print("getting all orders")
        if orders:
            return {'orders': [order.json() for order in orders]}, 200
        return {'message': 'No orders found'}, 404


    @jwt_required()
    def post(self):
        """return all Orders[US10]
        
        Returns:
            dict: containing all Orders
        """
        user = current_identity.json()
        userId = user['id']
        req = request.get_json() 
        lines = req['lines']
        OrderModel.placeOrder(userId)
        for line in lines:
            OrderModel.placeOrderline(line)
        return {"message":"Je hebt succesvol een order geplaatst"}, 200
        

class updateOrder(Resource):
    def patch(self, id):
        """updates an order in admin account[US19]
        """
        req = request.get_json()
        print("order_req: ", req)
        return OrderModel.update_order(req, id)


class showOrders(Resource): 
        
    def get(self, id):
        """return all Orders for one user by id[US10/19]
        
        Returns:
            dict: containing all Orders by user id 
        """
        orders = OrderModel.getOrder(id)
        print("ok")
        if orders:
            return {'orders': [order.json() for order in orders]}, 200
        return {'message': 'No orders found'}, 404




