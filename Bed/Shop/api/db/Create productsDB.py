import sqlite3
import csv
conn = sqlite3.connect('api/db/webshop.db')
cur = conn.cursor()

command2 = """CREATE TABLE IF NOT EXISTS 
products (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        categoryID INTEGER NOT NULL,
        supplier TEXT NOT NULL,
        date_added DATE NOT NULL,
        stock INTEGER NOT NULL,
        CONSTRAINT FK_categoryID FOREIGN KEY (categoryID) REFERENCES categories(id)
        ) """

cur.execute(command2)
print("Tabel products is aangemaakt")

fname=input('Enter the csv file name: ')
if len(fname) < 1 : fname= "producten.csv"

with open(fname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter= ';')
    for row in csv_reader:
        print(row)
        code=row[0]
        title=row[1]
        description=row[2]
        categoryID=row[3]
        price=row[4]
        supplier=row[5]
        date_added=row[6]
        stock=row[7]
      
        cur.execute('''INSERT INTO products(code, title, description, categoryID, price, supplier, date_added, stock)
            VALUES (?,?,?,?,?,?,?,?)''',(code, title, description, categoryID, price, supplier, date_added, stock))
        
conn.commit()
conn.close()