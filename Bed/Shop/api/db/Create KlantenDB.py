import sqlite3
import csv
conn = sqlite3.connect('api/db/webshop.db')
cur = conn.cursor()

command1 = """CREATE TABLE IF NOT EXISTS 
users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        infix TEXT NULL,
        lastname TEXT NOT NULL,
        street TEXT NOT NULL,
        housenumber INT NOT NULL,
        adjective TEXT NULL,
        zipcode TEXT NOT NULL,
        city TEXT NOT NULL,
        country INT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        newsletter INT NULL
        ) """


cur.execute(command1)
print("Tabel users is aangemaakt")

fname=input('Enter the csv file name: ')
if len(fname) < 1 : fname= "klanten.csv"

with open(fname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter= ';')
    for row in csv_reader:
        print(row)
        firstname=row[0]
        infix=row[1]
        lastname=row[2]
        street=row[3]
        housenumber=row[4]
        adjective=row[5]
        zipcode=row[6]
        city=row[7]
        country=row[8]
        email=row[9]
        password=row[10]
        newsletter=row[11]
        cur.execute('''INSERT INTO users(firstname, infix, lastname, street, housenumber, adjective, zipcode, city, country, email, password, newsletter)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(firstname, infix, lastname, street, housenumber, adjective, zipcode, city, country, email, password, newsletter))
        
conn.commit()
conn.close()