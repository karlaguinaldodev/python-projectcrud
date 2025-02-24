import psycopg2

def db_connect():
    conn = psycopg2.connect(
        host="localhost",
        database="python_project",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()

    # Drop the table if it exists
    # cur.execute('DROP TABLE IF EXISTS users;')

    # # Create the users table
    # cur.execute('''
    #     CREATE TABLE users (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(100) NOT NULL,
    #         age INT NOT NULL,
    #         address VARCHAR(255) NOT NULL
    #     );
    # ''')

    # # Insert sample data
    # cur.execute('''
    #     INSERT INTO users (name, age, address)
    #     VALUES 
    #     ('John Doe', 25, '123 Main St'),
    #     ('Jane Smith', 30, '456 Oak Ave'),
    #     ('Alice Johnson', 22, '789 Pine Rd'),
    #     ('Bob Brown', 35, '101 Elm St'),
    #     ('Angelo AGuinaldo', 22, 'Bugtong na Pulo, Lipa');
    # ''')

    # conn.commit()
    # cur.close()
    # conn.close()
    # print("Database initialized and data inserted.")
