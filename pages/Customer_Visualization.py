import streamlit as st
from PIL import Image
import base64
import matplotlib.pyplot as plt
import pandas as pd


from helpers import connection as conn
from helpers.Insurehub_Login import login_snippet



if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.toast("You need to login to access this page.")
    user_logged_in = login_snippet(key="buy_or_renew_login")


if st.session_state.user_logged_in:
    connection = conn.pgsql_connect()
    cur = connection.cursor()

    logo = "./images/profile_3135715.png"
    image = Image.open(logo)

    # Function to convert image to Base64
    def get_image_as_base64(path):
        with open(path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{data}"
        
    def get_base64_of_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()
        
    def set_background_from_local_file(path):
        base64_string = get_base64_of_file(path)
        # CSS to utilize the Base64 encoded string as a background
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        
    set_background_from_local_file('./images/login_background.png')
        
        
        
    image_base64 = get_image_as_base64(logo)

    st.markdown(f"""
                <a href="/" style="color:white;text-decoration: none;">
                    <div style="display:table;margin-top:-15 rem;margin-left:0%; display: flex;">
                        <img src="{image_base64}" alt="Insurehub Logo" style="width:50px;height:40px;margin-left:750px; flex:2;" </img>
                        <span style="padding:10px; flex:2;">{st.session_state['username']}</span>
                    </div>
                </a>
                <br>
                    """, unsafe_allow_html=True)

    custId = '3E6BA8C7-DCA6-7296-2DD1-729B1B1731D6'

    # Define a function to fetch the total number of policies held by a specific customer
    def fetch_total_policies(connection, customer_id):
        query = """
        SELECT COUNT(pu.policy_id) AS total_policies
        FROM insurehub.purchases pu
        WHERE pu.cust_id = %s;
        """
        # Execute the query with the specified customer ID
        cur = connection.cursor()
        cur.execute(query, (custId,))
        # Fetch the result
        result = cur.fetchone()
        # Close the cursor
        cur.close()
        # Return the total number of policies held by the customer
        return result[0] if result else 0
            
    def fetch_earliest_policy_end_date(connection, cust_id):
        query = """
        SELECT MIN(p.end_date) AS earliest_end_date
        FROM insurehub.policy p
        JOIN insurehub.purchases pu ON p.policy_id = pu.policy_id
        WHERE pu.cust_id = %s AND p.status = 'active';
        """
        # Execute the query with the specified customer ID and status as 'active'
        cur = connection.cursor()
        cur.execute(query, (cust_id,))
        # Fetch the result
        result = cur.fetchone()
        # Close the cursor
        cur.close()
        # Return the earliest policy end date for active policies
        return result[0] if result else None

    # Display a header for the section
    st.header("📊 Customer Dashboard")

    # Fetch the total number of policies held by the specified customer
    total_policies = fetch_total_policies(connection, custId)
    # Display the total number of policies as a sentence
    st.write(f"🔶 Your total policy count: {total_policies}")


    # Fetch the earliest policy end date for the specified customer
    earliest_end_date = fetch_earliest_policy_end_date(connection, custId)
    # Display the earliest policy end date as a sentence
    st.write(f"🔶 Your earliest renewal date of a policy is on: {earliest_end_date}")
    def fetch_total_claims(connection, cust_id):
        query = """
        SELECT COUNT(*) AS total_claims
        FROM insurehub.claim cl
        JOIN insurehub.policy p ON cl.policy_id = p.policy_id
        JOIN insurehub.purchases pu ON p.policy_id = pu.policy_id
        WHERE pu.cust_id = %s;
        """
        # Execute the query with the specified customer ID
        cur = connection.cursor()
        cur.execute(query, (cust_id,))
        # Fetch the result
        result = cur.fetchone()
        # Close the cursor
        cur.close()
        
        # Return the total number of claims
        return result[0] if result else 0

    # Fetch the total claims for the specified customer
    total_claims = fetch_total_claims(connection, custId)

    # Display the total number of claims as a sentence
    st.write(f"🔶 Total number of claims: {total_claims}")

    # Your existing function to fetch the count of active and expired policies for a specific customer
    def fetch_policy_status_counts(connection, cust_id):
        query = """
        SELECT 
            p.status, COUNT(p.policy_id) AS count
        FROM insurehub.policy p
        JOIN insurehub.purchases pu ON p.policy_id = pu.policy_id
        WHERE pu.cust_id = %s
        GROUP BY p.status;
        """
        # Execute the query with the specified customer ID
        cur = connection.cursor()
        cur.execute(query, (cust_id,))
        # Fetch the results
        results = cur.fetchall()
        # Close the cursor
        cur.close()

        # Initialize counts dictionary
        counts = {'active': 0, 'expired': 0}

        # Process results and populate counts dictionary
        for status, count in results:
            counts[status] = count

        return counts

    # Fetch the count of active and expired policies for the specified customer
    policy_status_counts = fetch_policy_status_counts(connection, custId)

    # Define labels and counts for the bar graph
    labels = ['Active Policies', 'Expired Policies']
    counts = [policy_status_counts.get('active', 0), policy_status_counts.get('expired', 0)]

    # Define colors for the bar graph
    colors = ['green', 'red']

    # Create the bar graph
    fig, ax = plt.subplots(figsize=(2, 1))  # Adjust the figure size as desired

    bar_width = 0.5  # Adjust the width of the bars; default is usually around 0.8
    bars = ax.bar(labels, counts, color=colors, width=bar_width)

    # Add title and labels
    ax.set_title("Your Policy Status", fontsize=6)
    ax.set_xlabel("Policy Status", fontsize=4)
    ax.set_ylabel("Count", fontsize=4)
    ax.set_xticklabels(labels, fontsize=4)
    ax.tick_params(axis='y', labelsize=4)
    y_max = max(counts)
    ax.set_yticks(range(y_max + 1))
    # Display the bar graph using Streamlit
    st.pyplot(fig)
        
    # Define a function to fetch policy names and their coverage amounts for a specific customer
    def fetch_policy_coverage(connection, cust_id):
        query = """
        SELECT 
            p.policy_id,
            pr.product_name,
            p.tot_coverage_amt
        FROM insurehub.policy p
        JOIN insurehub.purchases pu ON p.policy_id = pu.policy_id
        JOIN insurehub.product pr ON p.product_id = pr.product_id
        WHERE pu.cust_id = %s;
        """
        # Execute the query with the specified customer ID
        cur = connection.cursor()
        cur.execute(query, (cust_id,))
        # Fetch the results
        results = cur.fetchall()
        # Close the cursor
        cur.close()
        # Extract policy names and coverage amounts from results
        policy_names = []
        coverage_amounts = []

        for policy_id, product_name, tot_coverage_amt in results:
            policy_names.append(product_name)
            coverage_amounts.append(tot_coverage_amt)

        return policy_names, coverage_amounts

    # Fetch policy names and their coverage amounts for the specified customer
    policy_names, coverage_amounts = fetch_policy_coverage(connection, custId)

    # Create the bar graph
    fig, ax = plt.subplots(figsize=(2, 1))  # Adjust the figure size as desired

    bar_width = 0.4  # Adjust the width of the bars; default is usually around 0.8
    bars = ax.bar(policy_names, coverage_amounts, color='blue', width=bar_width)

    # Add title and labels
    ax.set_title("Policy Names vs. Coverage Amounts", fontsize=6)
    ax.set_xlabel("Policy Names", fontsize=4)
    ax.set_ylabel("Coverage Amount ($)", fontsize=4)
    ax.tick_params(axis='y', labelsize=4)
    
    # Set x-axis labels to have a smaller font size to fit more labels on the graph
    ax.set_xticklabels(policy_names, fontsize=4, rotation=45, ha='right')

    # Display the bar graph using Streamlit
    st.pyplot(fig)


