import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
