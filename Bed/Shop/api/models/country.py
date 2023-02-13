import sqlite3
import os

class CountryModel:

    def __init__(self, id, name):
        """CountryModel constructor

        Args:
            id (int): database id
            name (string): countryname
        """
        self.id = id
        self.name = name


    @classmethod
    def find(cls, id):
        """returns one userrole in the database

        Returns:
            list: one userrole
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM countries WHERE id=?", [id])
        row = cur.fetchone()
        conn.close()
        country = CountryModel(row[0], row[1])
        return country
    

    @classmethod
    def find_all(cls):
        """returns all countries in the database

        Returns:
            list: all countries
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM countries;"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        # Create an empty list
        countries = list()
        for row in rows:
            countries.append(CountryModel(row[0], row[1]))
        return countries
    

    @classmethod
    def add(cls, args):
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        name = args['name']
        cur.execute('''INSERT INTO countries(name)
            VALUES (?)''',(name,))
        conn.commit()
        conn.close()
        return {"message":"Land is toegevoegd"}, 200


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        return self.__dict__  
