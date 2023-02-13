from flask import request
import os
import sqlite3
from models.user import UserModel
from models.order_line import OrderLineModel
from models.product import ProductModel
import datetime
import time
from flask_jwt import JWT, jwt_required, current_identity

class OrderModel:
    
    def __init__(self, id, date, paid, shipped, user):
        """OrderModel constructor

        Args:
            id (int): database id
            date (string): 
            paid (int): 0 for no, 1 for yes
            shipped (int): 0 for no, 1 for yes
            user (int): user id
        """
        self.id = id
        self.date = date
        self.paid = paid
        self.shipped = shipped
        self.user = user


    @classmethod #post request Submit an order in frontend 
    def placeOrder(cls, userId):
        """Place order in the database

        Returns:
            Message: Order is placed
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        today = datetime.date.today()
        order = cur.execute('INSERT INTO orders(date, paid, shipped, user) VALUES(?,?,?,?)', (today, 0, 0, userId))
        conn.commit()
        conn.close()
        return order
    

    @classmethod 
    def placeOrderline(cls, line):
        """
        Places orderlines in the database
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        productId = line['product']
        amount = line['amount']
        product = ProductModel.find_product(productId)
        price = product.price_vat
        total_price = amount * price
        order_id = OrderModel.findOrder()
        print("orderID: ", order_id)
        cur.execute('INSERT INTO order_lines(product, order_id, amount, total_price) VALUES(?,?,?,?)', (productId, order_id, amount, total_price)) 
        conn.commit()
        conn.close()
        return product


    @classmethod
    @jwt_required()
    def findOrder(cls): 
        """
        find the last placed order by user id
        """   
        user = current_identity.json()
        userId = user['id']
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute("SELECT max(id) FROM orders WHERE user=?", [userId]) 
        row = cur.fetchone()
        id = row[0]
        conn.close()
        return id


    @classmethod #get request showOrders
    def getOrder(cls, id):     
        """
        Selects all orders from one user by id
        Returns: Dict with all orders for one user [US10/19]
        """             
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM orders WHERE user=?", [id])
        rows = cur.fetchall()
        conn.close()
        orders = list()
        for row in rows:
            orders.append(OrderModel(row[0], row[1], row[2], row[3], row[4]))
        print("Orders for user", id)
        return orders


    @classmethod
    def update_order(cls, args, id):
        """updates an order from the database [US19]

        Returns:
            Message: Succesfully updated order
        """
        print("args: ", args, "order_id: ", id)

        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        if 'paid' in args:
            paid = args['paid']
            cur.execute('UPDATE orders set paid=? WHERE id=?', (paid, id))
            print("betaling aangepast")
            conn.commit()
            conn.close()
            return {"message":"Status betaling succesvol gewijzigd"}, 200
        elif 'shipped' in args:
            shipped = args['shipped']
            cur.execute('UPDATE orders set shipped=? WHERE id=?', (shipped, id))
            print("status verzending aangepast")
            conn.commit()
            conn.close()
            return {"message":"Status verzending succesvol gewijzigd"}, 200


    @classmethod
    def find_all(cls):
        """returns all orders in the database

        Returns:
            list: all orders
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM orders;"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        orders = list()
        for row in rows:
            orders.append(OrderModel(row[0], row[1], row[2], row[3], row[4]))
        return orders


    def get_orderlines(self):
        """Get OrderLines

        Returns:
            dict: order_lines
        """        
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM order_lines WHERE order_id=?", [self.id])
        rows = cur.fetchall()
        conn.close()
        orderlines = list()
        for row in rows:
            orderlines.append(OrderLineModel(row[0], row[1], row[2], row[3], row[4]))
        return orderlines


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        self_dict = self.__dict__ 
        user = UserModel.userId(self.user)
        self_dict["user"] = user.json()
        lines = self.get_orderlines()
        if lines:
            self_dict["order_lines"] = [line.json() for line in lines]
        return self_dict