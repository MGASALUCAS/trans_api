import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    # conn = sqlite3.connect('database.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT,
                 email TEXT, password TEXT)''')
    conn.commit()
    conn.close()


def create_table2():
    conn = create_connection()
    c = conn.cursor()
    
    # Create admin table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS instructors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL,
                  email TEXT NOT NULL, 
                  password TEXT NOT NULL)''')
    
    
    conn.commit()
    conn.close()



