import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def pgsql_connect():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USERNAME"), 
            password=os.getenv("DB_PASSWORD"), 
            host=os.getenv("DB_HOST"), 
            port=os.getenv("DB_PORT") 
        )
        print("Connected to the database.")

        return conn 
    
    
    except Exception as e:
        print(f"Unable to connect to the database: {e}")


# ## Delete Functionality
connection = pgsql_connect()
cur = connection.cursor()
# #cur.execute("delete from insurehub.purchases where policy_id = '2B2A26FB-DE7F-80C8-E66D-BCBAC79A5282'")
# print('Record deleted successfully')
# connection.commit()

# ## Insert Functionality
# #cur.execute("Insert into insurehub.purchases values ('C778A722-2A23-1182-36B5-A3DB69265960','2B2A26FB-DE7F-80C8-E66D-BCBAC79A5282')")
# print('Record inserted successfully')
# connection.commit()

# ## Update query
# cur.execute("UPDATE insurehub.customer SET first_name = 'Luis' WHERE cust_id = '3E6BA8C7-DCA6-7296-2DD1-729B1B1731D6'")
# print('Record updated successfully')
# connection.commit()

