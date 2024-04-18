from helpers import connection as conn
import streamlit as st
import matplotlib.pyplot as plt

connection = conn.pgsql_connect()
cur = connection.cursor()

def get_data():
    try:
        with connection.cursor() as curs:
            curs.execute("""
                select  product_name , cnt from(
                select count(policy_id) as cnt, pr.product_id, product_name from
                insurehub.product pr
                left join
                insurehub.policy pl
                on pr.product_id = pl.product_id
                group by pr.product_id, product_name) a
            """)
            data = curs.fetchall()
            return data
    finally:
        cur.close()

def plot_data(data):
    x, y = zip(*data)  # This assumes data is a list of tuples (x, y)
    plt.figure()
    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel('Products')
    plt.ylabel('Number of Policies')
    plt.xticks(rotation=90)
    plt.title('Bar Chart of Product vs Policies')
    plt.grid(True)
    st.pyplot(plt)

def main():
    data = get_data()
    plot_data(data)

if __name__ == "__main__":
    st.title('Data Visualization for Admin role:')
    main()