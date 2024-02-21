import psycopg2

def pgsql_connect():
    try:
        conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="dbms5614", 
            host="localhost", 
            port="5432" 
        )
        print("Connected to the database.")
    except Exception as e:
        print(f"Unable to connect to the database: {e}")

    cur = conn.cursor()

    cur.execute("SELECT * FROM insurehub.policy;")
    rows = cur.fetchall()
    for row in rows:
        print(row)


pgsql_connect()

