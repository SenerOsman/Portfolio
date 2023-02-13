from models.category import CategoryModel
import sqlite3
import os
import datetime
import re

class ProductModel:
    
    def __init__(self, id, code, title, description, price, stock, categoryID):
        """ProductModel constructor

        Args:
            id (int): database id
            code (string): product-code
            title (string): 
            description (string): 
            price (int): in cents
            category (int): category id 
            stock (int): amount in stock
        """
        self.id = id
        self.code = code
        self.title = title
        self.description = description
        self.price_vat = round(price*1.21)
        self.stock = stock
        self.category = categoryID


    @classmethod
    def find_all(cls):
        """returns all products in the database

        Returns:
            list: all products
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM products"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        products = list()
        for row in rows:
            products.append(ProductModel(row[0], row[1], row[2], row[3], row[4], row[8], row[5]))
        return products


    @classmethod
    def find_category(cls, id):
        # Create an empty list
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE categoryID =? ORDER BY title', [id])
        product_rows = cur.fetchall()
        conn.close()
        product = list()
        for product_row in product_rows:
            product.append(ProductModel(product_row[0], product_row[1], product_row[2], product_row[3], product_row[4], product_row[8], product_row[5]))
        return product
        
    
    @classmethod
    def find_product(cls, id):
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE id =?', [id])
        product_row = cur.fetchone()
        if product_row:
            product = ProductModel(product_row[0], product_row[1], product_row[2], product_row[3], product_row[4], product_row[8], product_row[5])
        else:
            return None
        return product


    @classmethod
    def product_search(cls, query):
        """[searches items by query input]
        Returns:
           products that match the search query
        """        
        products = list()

        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        for product in cur.execute("SELECT * FROM products WHERE title LIKE :search OR description LIKE :search ORDER BY title",{"search":'%'+query+'%'}):
            products.append(ProductModel(product[0], product[1], product[2], product[3], product[4], product[8], product[5]))
        return products


    @classmethod
    def add_product(self, args):
        """adds products in the database

        Returns:
            Message: Succesfully added product
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        print("args: ",args)
        code = args['code']
        title = args['title']
        description = args['description']
        price_none_vat = args['price_vat']
        print("price_vat: ", price_none_vat)
        price = round(int(price_none_vat)/1.21)
        category = args['category']
        stock = args['stock']
        #checks productcode validation
        if len(args['code']) < 5:
            return {'message': 'Productcode format is AA-00 of AAA-000'}, 400
        elif re.search('[A-Z]',args['code']) is None:
            return {'message': 'Productcode format is AA-00 of AAA-000'}, 400
        elif re.search('[0-9]',args['code']) is None:
            return {'message': 'Productcode format is AA-00 of AAA-000'}, 400
        elif args['code'].find('-')== -1:
            return {'message': 'Productcode format is AA-00 of AAA-000'}, 400

        #title validation
        elif len(args['title']) <= 2:
            return {'message': 'Titel moet minimaal 3 karakters bevatten'}, 400
        #description validation
        elif len(args['description']) <= 5:
            return {'message': 'Beschrijving moet minimaal 5 karakters hebben'}, 400

        #price validation
        elif len(args['price_vat']) <= 2:
            return {'message': 'Prijs moet minimaal 1 euro zijn'}, 400
        elif re.search('[0-9]',args['price_vat']) is None:
            return {'message': 'Productcode moet minimaal 2 cijfers bevatten'}, 400
        elif re.search('[a-z]',args['price_vat']):
            return {'message': 'Prijs mag alleen uit cijfers bestaan'}, 400
        elif re.search('[A-Z]',args['price_vat']):
            return {'message': 'Prijs mag alleen uit cijfers bestaan'}, 400

        #stock validation
        elif re.search('[a-z]',args['stock']):
            return {'message': 'Voorraad dient alleen uit cijfers te bestaan'}, 400
        elif re.search('[A-Z]',args['stock']):
            return {'message': 'Voorraad dient alleen uit cijfers te bestaan'}, 400
        elif re.search('[0-9]',args['stock']) is None:
            return {'message': 'Voorraad is onjuist ingevuld'}, 400
        today = datetime.date.today()
        cur.execute('''INSERT INTO products(code,title,description,price,categoryID,supplier,date_added,stock)
            VALUES (?,?,?,?,?,?,?,?)''',(code,title,description,price,category,"TBA",today,stock))
        conn.commit()
        conn.close()
        return {"message":"Product is toegevoegd"}, 200


    @classmethod
    def update_product(cls, args, id):
        """updates a product from the database [US13]

        Returns:
            Message: Succesfully updates product
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        code = args['code']
        title = args['title']
        description = args['description']
        price_none_vat = args['price_vat']
        price = round(int(price_none_vat)/1.21)
        category = args['category']
        stock = args['stock']
        #productcode validation
        if len(args['code']) < 5:
            return {'message': 'Productcode format is AA-00 of AAA-000'}, 400
        elif re.search('[A-Z]',args['code']) is None:
            return {'message': 'Productcode moet minimaal 2 hoofdletters bevatten'}, 400
        elif re.search('[0-9]',args['code']) is None:
            return {'message': 'Productcode moet minimaal 2 cijfers bevatten'}, 400
        elif args['code'].find('-')== -1:
            return {'message': 'Productcode moet een - teken bevatten'}, 400

          #title validation
        elif len(args['title']) <= 2:
            return {'message': 'Titel moet minimaal 3 karakters bevatten'}, 400
        #description validation
        elif len(args['description']) <= 5:
            return {'message': 'Beschrijving moet minimaal 5 karakters hebben'}, 400

        #price validation
        elif len(args['price_vat']) <= 2:
            return {'message': 'Prijs moet minimaal 1 euro zijn'}, 400
        elif re.search('[0-9]',args['price_vat']) is None:
            return {'message': 'Productcode moet minimaal 2 cijfers bevatten'}, 400
        elif re.search('[a-z]',args['price_vat']):
            return {'message': 'Prijs mag alleen uit cijfers bestaan'}, 400
        elif re.search('[A-Z]',args['price_vat']):
            return {'message': 'Prijs mag alleen uit cijfers bestaan'}, 400

        #stock validation
        elif re.search('[a-z]',args['stock']):
            return {'message': 'Voorraad dient alleen uit cijfers te bestaan'}, 400
        elif re.search('[A-Z]',args['stock']):
            return {'message': 'Voorraad dient alleen uit cijfers te bestaan'}, 400
        elif re.search('[0-9]',args['stock']) is None:
            return {'message': 'Voorraad is onjuist ingevuld'}, 400
        cur.execute("UPDATE products set code=?,title=?,description=?,price=?,categoryID=?,stock=? WHERE id="+ str(id),(code,title,description,price,category,stock))
        conn.commit()
        conn.close()
        return {"message":"Product is gewijzigd"}, 200


    @classmethod
    def delete_product(self, id):
        """deletes a product from the database

        Returns:
            Message: Succesfully deletes product
        """
        print("id_deletedproduct: ", id)
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        # orders = list()
        # cur.execute('SELECT order_id FROM order_lines WHERE product=?', [id])
        # order_lines = cur.fetchall()
        # print("lines: ", order_lines)

        # for i in range(len(order_lines)):
        #     print(order_lines[i])
        #     cur.execute('SELECT * FROM orders WHERE id=?', (order_lines[i]))
        #     orders.append(cur.fetchall)
        #     print("i: ", i)
        # print("orders: ", orders)
        # if '0' in orders:
        #     return {"message"  : "Dit product maakt nog deel uit van een lopende order"}
        cur.execute('DELETE FROM products WHERE id=?', [id])
        conn.commit()
        conn.close()
        return {"message":"Product is verwijderd"}, 200


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """    
        self_dict=self.__dict__
        categorie = CategoryModel.find(self.category)
        self_dict["category"] = categorie.json()
        return self_dict
