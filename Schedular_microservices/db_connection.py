import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='vijay',
        user='postgres',
        password='root'
    )

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        interval VARCHAR(50) NOT NULL,
        job_details TEXT NOT NULL,
        last_run TIMESTAMP,
        next_run TIMESTAMP
    );
    ''')
    print('Table created successfully')
    conn.commit()
    cursor.close()
    conn.close()

