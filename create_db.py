import sqlite3

def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employee(
        eid INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        contact TEXT,
        name TEXT,
        dob TEXT,
        doj TEXT,
        email TEXT,        
        pass TEXT,
        utype TEXT,
        address TEXT,
        salary TEXT
    )""")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS supplier(
        invoice INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        desc TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS category(
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS product(
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier TEXT,
        Category TEXT,
        name TEXT,
        price TEXT,
        qty TEXT,
        status TEXT
    )""")

    con.commit()
    con.close()

create_db()
