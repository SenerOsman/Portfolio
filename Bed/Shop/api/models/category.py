import sqlite3
import os

class CategoryModel:
    
    def __init__(self, id, name):
        """CategoryModel constructor

        Args:
            id (int): database id
            name (string): display name
        """
        self.id = id
        self.name = name
    
    @classmethod
    def find_all(cls):
        """returns all categories in the database

        Returns:
            list: all categories
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM categories ORDER BY name;"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        categories = list()
        for row in rows:
            categories.append(CategoryModel(row[0], row[1]))
        return categories


    @classmethod
    def find(cls, id):
        """returns one category by ID

        Returns:
            list: category
        """        
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM categories WHERE id =?', [id])
        category_row = cur.fetchone()
        category = CategoryModel(category_row[0], category_row[1])
        return category


    @classmethod
    #Haal een category op uit de database
    def addCategory(self, args):
        """Adds a category to the database

        Returns: 
            Message":Categorie is toegevoegd
        """    
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        name = args['name']
        if len(args['name']) < 3:
            return {'message': 'Een categorie moet uit minstens 3 karakters bestaan'}, 400
        cur.execute('''INSERT INTO categories(name)
            VALUES (?)''',(name,))
        conn.commit()
        conn.close()
        return {"message":"Categorie is toegevoegd"}, 200


    @classmethod
    def update_cat(cls, args, id):
        """Updates a category from the database [US13]

        Returns:
            Message: Succesfully updates category
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        name = args['name']
        if len(args['name']) < 3:
            return {'message': 'Een categorie moet uit minstens 3 karakters bestaan'}, 400
        cur.execute("UPDATE categories set name=? WHERE id=?",(name, id))
        conn.commit()
        conn.close()
        return {"message":"Categorie is succesvol gewijzigd"}, 200


    @classmethod
    def delete(self, id):
        """deletes a product from the database

        Returns:
            Message: Succesfully deletes product
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute('DELETE FROM categories WHERE id=?', [id])
        conn.commit()
        conn.close()
        return {"message":"Categorie is verwijderd"}, 200


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        return self.__dict__        