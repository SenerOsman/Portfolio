import sqlite3
import os
import re
import json
import datetime
import secrets

from models.country import CountryModel
from models.userrole import UserroleModel
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask, jsonify, request
from flask_restful import Resource


class UserModel:

    def __init__(self, id, email, password, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, country, userrole):
        """UserModel constructor

        Args:
            id (int): database id
            email (string): 
            password (string): 
            firstname (string): 
            infix (string): can be emtpy
            lastname (string): 
            street (string): 
            housenumber (string): with adjective (23b)
            zipcode (string): 
            city (string): 
            newsletter (int): 1 for yes, 0 for no
            userrole (int): userrole id
            country (int): country id
        """
        self.id = id
        self.email = email
        self.password = password
        self.firstname = firstname
        self.infix = infix
        self.lastname = lastname
        self.street = street
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city
        self.newsletter = newsletter
        self.country = country
        self.userrole = userrole


    @classmethod
    def register(cls, args):
        """Creates a new account

        Returns: valid data into the database, table users  
            
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        infix = args['infix']
        lastname = args['lastname']
        street = args['street']
        housenumber = args['housenumber']
        zipcode = args['zipcode']
        city = args['city']
        newsletter = args['newsletter']
        country = args['country']
        #password checks
        if len(args['password']) < 8:
            return {'message': 'Voer een wachtwoord in met minimaal 8 karakters '}, 400
        elif re.search('[A-Z]',args['password']) is None:
            return {'message': 'Je wachtwoord moet minimaal 1 hoofdletter bevatten'}, 400
        elif re.search('[0-9]',args['password']) is None:
            return {'message': 'Je wachtwoord moet minimaal 1 cijfer bevatten'}, 400
        
        #email checks
        elif len(args['email']) <= 5:
            return {'message': 'Email adres is te kort'}, 400
        elif args['email'].find('@')== -1:
            return {'message': 'Email adres is incorrect'}, 400
        elif args['email'].find('.')== -1:
            return {'message': 'Email adres is incorrect'}, 400
        
        #checks if the housenumber contains digits only
        elif not args['housenumber'].isdigit():
            return {'message': 'Huisnummer moet uit cijfers bestaan'}, 400
        
        #checks if all mandatory have an input
        elif len (args['firstname']) < 1: 
             return {'message': 'Vul een voornaam in'}, 400
        elif len (args['lastname']) < 1: 
             return {'message': 'Vul een achternaam in'}, 400
        elif len (args['street']) < 1: 
             return {'message': 'Vul een straatnaam in'}, 400
        elif len (args['city']) < 1: 
             return {'message': 'Vul een stad in'}, 400
    
        elif args['country'] == '1': 
            if re.match('^[0-9]{4}[a-zA-Z]{2}$', args['zipcode']):
                cur.execute('''INSERT INTO users(email, password, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, userrole, country)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(email, password, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, 1, country))
                conn.commit()
                conn.close()
                return {"message":"Registratie succesvol"}, 200
            else: 
                return {"message": "Postcode voor het gekozen land is onjuist"}, 400
        elif args['country'] == '2':
            if re.match('^[0-9]$', args['zipcode']):
                cur.execute('''INSERT INTO users(email, password, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, userrole, country)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(email, password, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, 1, country))
                conn.commit()
                conn.close()
                return {"message":"Registratie succesvol"}, 200
            else: 
                return {"message": "Postcode voor het gekozen land is onjuist"}, 400


    @classmethod
    def login(cls,  email, password):
        """Gets an user from the database

        Returns:
            list: logged in user
        """        
        con = sqlite3.connect("db/webshop.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?",(email, password))
        row = cur.fetchone()
        if row:
            user = UserModel(row[0], row[10], row[11], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[12], row[9], row[13])
            return user


    @classmethod
    def find_all(cls):
        """returns all users in the database
        Returns:
            list: all products
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        query="SELECT * FROM users"
        cur.execute(query,list())
        rows = cur.fetchall()
        conn.close()
        users = list()
        for row in rows:
            users.append(UserModel(row[0], row[10], row[11], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[12], row[9], row[13]))
        return users


    @classmethod
    def userId(cls, id): 
        """
        Collects the user information for the order.json
        """  
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", [id])
        row = cur.fetchone()
        conn.close()
        if row:
            user = UserModel(row[0], row[10], row[11], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[12], row[9], row[13])
        return user
    

    @classmethod
    def update(cls, args, id):
        """updates a user from the database [US16]

        Returns:
            Message: Succesfully updates user
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        email = args['email']
        firstname = args['firstname']
        infix = args['infix']
        lastname = args['lastname']
        street = args['street']
        housenumber = args['housenumber']
        zipcode = args['zipcode']
        city = args['city']
        newsletter = args['newsletter']
        country = args['country']
        
        #email checks
        if len(args['email']) <= 5:
            return {'message': 'Email adres is te kort'}, 400
        elif args['email'].find('@')== -1:
            return {'message': 'Email adres is incorrect'}, 400
        elif args['email'].find('.')== -1:
            return {'message': 'Email adres is incorrect'}, 400
        
        #checks if the housenumber contains digits only
        elif not args['housenumber'].isdigit():
            return {'message': 'Huisnummer moet uit cijfers bestaan'}, 400
        
        #checks if all mandatory have an input
        elif len (args['firstname']) < 1: 
             return {'message': 'Vul een voornaam in'}, 400
        elif len (args['lastname']) < 1: 
             return {'message': 'Vul een achternaam in'}, 400
        elif len (args['street']) < 1: 
             return {'message': 'Vul een straatnaam in'}, 400
        elif len (args['city']) < 1: 
             return {'message': 'Vul een stad in'}, 400
    
        elif args['country'] == '1': 
            if re.match('^[0-9]{4}[a-zA-Z]{2}$', args['zipcode']):
                cur.execute("UPDATE users SET email=?, firstname=?, infix=?, lastname=?, street=?, housenumber=?, zipcode=?, city=?, country=?, newsletter=? WHERE id="+ str(id), (email, firstname, infix, lastname, street, housenumber, zipcode, city, country, newsletter))
                conn.commit()
                conn.close()
                return {"message":"Account succesvol gewijzigd"}, 200
            else: 
                return {"message": "Postcode voor het gekozen land is onjuist"}, 400
        elif args['country'] == '2':
            if re.match('^[0-9]$', args['zipcode']):
                cur.execute("UPDATE users SET email=?, firstname=?, infix=?, lastname=?, street=?, housenumber=?, zipcode=?, city=?, country=?, newsletter=? WHERE id="+ str(id), (email, firstname, infix, lastname, street, housenumber, zipcode, city, country, newsletter))
                conn.commit()
                conn.close()
                return {"message":"Account succesvol gewijzigd"}, 200
            else: 
                return {"message": "Postcode voor het gekozen land is onjuist"}, 400


    @classmethod
    def delete(self, id):
        """deletes a user from the database

        Returns:
            Message: Succesfully deletes user
        """
        conn = sqlite3.connect("db/webshop.db")
        cur = conn.cursor()
        print("id_deleteduser: ", id)
        cur.execute('DELETE FROM users WHERE id=?', [id])
        conn.commit()
        conn.close()
        return {"message":"Gebruiker is verwijderd"}, 200

        
    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        self_dict = self.__dict__ 
        
        userrole = UserroleModel.find(self.userrole)
        self_dict["userrole"] = userrole.json()
        country = CountryModel.find(self.country)
        self_dict["country"] = country.json()

        return self_dict


class UserModel2:
    # Dit model gebruik ik om een UserModel zonder password terug te geven
    def __init__(self, id, email, firstname, infix, lastname, street, housenumber, zipcode, city, newsletter, userrole, country):
        """UserModel constructor

        Args:
            id (int): database id
            email (string): 
            password (string): 
            firstname (string): 
            infix (string): can be emtpy
            lastname (string): 
            street (string): 
            housenumber (string): with adjective (23b)
            zipcode (string): 
            city (string): 
            newsletter (int): 1 for yes, 0 for no
            userrole (int): userrole id
            country (int): country id
        """
        self.id = id
        self.email = email
        self.firstname = firstname
        self.infix = infix
        self.lastname = lastname
        self.street = street
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city
        self.newsletter = newsletter
        self.userrole = userrole
        self.country = country


    def json(self):
        """Returns a JSON version of the current object

        Returns:
            dict: the object
        """
        self_dict = self.__dict__ 
        
        userrole = UserroleModel.find(self.userrole)
        self_dict["userrole"] = userrole.json()
        country = CountryModel.find(self.country)
        self_dict["country"] = country.json()

        return self_dict

