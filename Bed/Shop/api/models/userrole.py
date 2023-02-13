import sqlite3
import os
import json

class UserroleModel:
    
    def __init__(self, id, name):
        """UserroleModel constructor

        Args:
            id (int): database id
            name (string): display name of the category
        """
        self.id = id
        self.name = name
    
    @classmethod
    def find_all(cls):
        """returns all userroles in the database

        Returns:
            list: all userroles
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM userrole;"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        # Create an empty list
        userroles = list()
        for row in rows:
            userroles.append(UserroleModel(row[0], row[1]))
        
        # return the list of userroles
        return userroles


    @classmethod
    def find(cls, id):
        """returns one userrole in the database

        Returns:
            list: one userrole
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM userrole WHERE id=?", [id])
        row = cur.fetchone()
        conn.close()
        userrole = UserroleModel(row[0], row[1])
        return userrole

    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        return self.__dict__   