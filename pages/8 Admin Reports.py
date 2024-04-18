from helpers import connection as conn
import streamlit as st
import matplotlib.pyplot as plt

connection = conn.pgsql_connect()
cur = connection.cursor()

def get_product_policy_data():
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

def get_claim_status_data():
    try:
        with connection.cursor() as curs:
            curs.execute("""
                select status, count(*) as cnt  from insurehub.claim
                group by status
            """)
            data = curs.fetchall()
            return data
    finally:
        cur.close()

def get_top_5_agents():
    try:
        with connection.cursor() as curs:
            curs.execute("""
                select name, cnt from
                (select count(*) as cnt, cust.agent_id, concat(rm.first_name, ' ', rm.last_name) as name
                from insurehub.customer cust
                join insurehub.relationship_manager rm
                on cust.agent_id = rm.agent_id
                group by cust.agent_id, concat(rm.first_name, ' ', rm.last_name)
                order by cnt desc
                limit 5) a
            """)
            data = curs.fetchall()
            return data
    finally:
        cur.close()

def get_avg_revenue():
    try:
        with connection.cursor() as curs:
            curs.execute("""
                select extract(year from payment_date) as year,
                round(avg(payment_amt), 2)
                from insurehub.payment
                group by extract(year from payment_date)
                order by extract(year from payment_date)
            """)
            data = curs.fetchall()
            return data
    finally:
        cur.close()

def get_sum_revenue():
    try:
        with connection.cursor() as curs:
            curs.execute("""
                select 
                concat(rm.first_name, ' ', rm.last_name) as name,
                sum(cast(tar_rev_per_mon as int)) from 
                insurehub.goal gl
                join
                insurehub.relationship_manager rm
                on gl.agent_id = rm.agent_id
                where status = 'Completed'
                group by concat(rm.first_name, ' ', rm.last_name)
            """)
            data = curs.fetchall()
            return data
    finally:
        cur.close()

def plot_top_5_agents(data):
    x, y = zip(*data)  # This assumes data is a list of tuples (x, y)
    plt.figure()
    plt.figure(figsize=(8, 4))
    plt.bar(x, y)
    plt.xlabel('Agents')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=90)
    plt.title('Top 5 High Performing Agents')
    plt.grid(True)
    st.pyplot(plt)

def plot_prod_policy_data(data):
    x, y = zip(*data)  # This assumes data is a list of tuples (x, y)
    plt.figure(figsize=(10, 6))
    plt.pie(y, labels=x, autopct='%1.1f%%')  # Plot pie chart with percentage labels
    plt.title('Product vs No. of Policies')
    st.pyplot(plt)

def plot_claim_status_data(data):
    x, y = zip(*data)  # This assumes data is a list of tuples (x, y)
    plt.figure(figsize=(8, 6))
    plt.pie(y, labels=x, autopct='%1.1f%%', startangle=90, wedgeprops={'width':0.6})  # Create a donut chart
    plt.title('Claims by status')
    st.pyplot(plt)

def plot_avg_rev(data):
    x, y = zip(*data) 
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Avg. Revenue')
    plt.xticks(rotation=90)
    plt.title('Avg. Revenue over the years')
    plt.grid(True)
    st.pyplot(plt)

def plot_sum_rev(data):
    names, revenues = zip(*data)  # Unpack names and revenues
    sizes = [rev / 10 for rev in revenues]  # Calculate bubble sizes proportionally, adjust the divisor as needed

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(names, revenues, s=sizes, alpha=0.5)  # Use revenues as sizes directly
    plt.xlabel('Agent Name')
    plt.ylabel('Sum of Revenue')
    plt.xticks(rotation=90)
    plt.title("Revenue by Agent's Goals:")
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.subheader("Distribution of Products by No. of Policies:")
    prod_policy_data = get_product_policy_data()
    plot_prod_policy_data(prod_policy_data)

    st.subheader("Top 5 High Performing Agents: 🌟")
    agents_data = get_top_5_agents()
    plot_top_5_agents(agents_data)

    st.subheader("Monitor Claim Status:")
    claim_data = get_claim_status_data()
    plot_claim_status_data(claim_data)

    st.subheader("Average Revenue vs Year:")
    rev_data = get_avg_revenue()
    plot_avg_rev(rev_data)

    st.subheader("Sum of Revenue through Goals:")
    rev_data = get_sum_revenue()
    plot_sum_rev(rev_data)

if __name__ == "__main__":
    st.title('Data Visualization for Admin role:')
    main()