import streamlit as st
from datetime import datetime
from PIL import Image
import base64
import uuid
from datetime import datetime , timedelta

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
        
    def getCustId(email):
        query = f"SELECT cust_id FROM insurehub.customer WHERE email = '{email}'"
        cur.execute(query)
        custId = cur.fetchall()
        return custId[0][0]
        
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
        
    def getProductDetails():
        cur.execute(f"select product_id, product_name, description from insurehub.product")
        
        rows = cur.fetchall()
        products_list = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
        
        return products_list
    
    def get_admin_id(email):
        query = f"SELECT admin_id FROM insurehub.admin WHERE email = '{email}'"
        cur.execute(query)
        custId = cur.fetchall()
        return custId[0][0]

    def handle_buy(product_name, product_id):
        # Save the selected product name to the session state
        st.session_state['selected_product'] = product_name
        st.session_state['selected_product_id'] = product_id
        # Redirect to the payment details page
        #st.session_state['show_payment_details'] = True
        st.session_state['show_policy_details'] = True 

    def show_policy_details():
        st.header(f"Coverage Details for: {st.session_state['selected_product']}")
        cur.execute(f"select coverage_desc from insurehub.product where product_id = '{st.session_state['selected_product_id']}'")
        
        row = cur.fetchall()
        if row:
            # Parse the JSON string into a Python list
            tuple = row[0]
            coverage_items = tuple[0]
            st.markdown("### Coverage Includes:")
            for item in coverage_items:
                st.markdown(f"""
                    <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.5);">
                    🚀 {item}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No details available for this product.")

        st.subheader("Rates tailored for you:")
        cur.execute(f"select rate_amount from insurehub.product where product_id = '{st.session_state['selected_product_id']}'")
        
        row = cur.fetchall()
        st.markdown(f"### $ {row[0][0]}")


        if st.button("Back to Explore plans"):
            st.session_state['show_policy_details'] = False
            st.rerun()
            return 

        
        # Continue button to proceed to payment
        if st.button("Continue to Payment"):
            st.session_state['show_payment_details'] = True
            st.session_state['show_policy_details'] = False  # Hide policy details
            st.rerun()


    # Define a function to add new products
    def add_product(product_name, description, coverage_desc):
        try:
            #admin_id='3457D733-E929-4BB1-9B82-B07A06BE76F3'
            admin_id = get_admin_id(st.session_state['username'])
            product_id = str(uuid.uuid4())
            # Split the coverage description into lines and store each line in a list
            coverage_lines = coverage_desc.split('\n')
        
            # Convert the list of lines into a PostgreSQL array string
            coverage_array_str = "{" + ",".join([f"'{line.strip()}'" for line in coverage_lines]) + "}"
        
            cur.execute("INSERT INTO insurehub.product (product_id, product_name, description, admin_id, coverage_desc) VALUES (%s, %s, %s, %s, %s)",
                    (product_id, product_name, description, admin_id, coverage_array_str))
            connection.commit()
            st.success("Product added successfully!")
        except Exception as e:
            st.error("An error occurred while adding the product:", e)
            connection.rollback()

    # Function to display payment details form and handle the transaction
    def show_payment_details():
        st.write(f"You have chosen to buy: {st.session_state['selected_product']}")
        
        with st.form("payment_form", clear_on_submit=True):
            name_on_card = st.text_input("Name on Card")
            card_number = st.text_input("Card Number", max_chars=16)
            expiration_date = st.date_input("Expiration Date")
            cvv = st.text_input("CVV", max_chars=3)
            submit_button = st.form_submit_button("Pay")

            if submit_button:
                # Generate a unique policy ID
                policy_id = str(uuid.uuid4()).upper()
                payment_id = str(uuid.uuid4())


                ### Hard coding details to be added to policy table. Must be changed later
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=365)
                coverage_amt = '100000'
                status = 'active'
                #custId = '2DECA7C8-395E-5B44-4A3B-C792143C9F45'
                custId= getCustId(st.session_state['username'])
                amount = 1000

                print(custId)

                #insert the new policy ID and other details into the policy table
                try:
                    cur.execute(f"INSERT INTO insurehub.policy VALUES ('{policy_id}', '{start_date}', '{end_date}', '{coverage_amt}', '{st.session_state['selected_product_id']}', '{status}' ) ")
                    connection.commit()

                    cur.execute(f"INSERT INTO insurehub.purchases VALUES ( '{custId}', '{policy_id}') ")
                    connection.commit()

                    cur.execute(f"INSERT INTO insurehub.payment VALUES ( '{payment_id}', '{amount}', '{start_date}', 'credit card' , '{policy_id}') ")
                    connection.commit()

                    st.success("Transaction was successful! Your policy ID is: " + policy_id)
                    st.success("Payment Id: " + payment_id)
                    
                    # Clean up session state after successful transaction
                    del st.session_state['selected_product']
                    del st.session_state['show_payment_details']
                except Exception as e:
                    st.error("An error occurred while processing your transaction.",)
                    connection.rollback()

        if st.button("Back to Policy Details"):
            st.session_state['show_payment_details'] = False
            st.session_state['show_policy_details'] = True
            st.rerun()
            return 


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

    if 'show_policy_details' not in st.session_state and 'show_payment_details' not in st.session_state:
        st.title('Explore our plans! ☂️')

    products = getProductDetails()

    if 'show_policy_details' not in st.session_state:
        st.session_state['show_policy_details'] = False

    if 'show_payment_details' not in st.session_state:
        st.session_state['show_payment_details'] = False

        if 'selected_product' not in st.session_state:
            st.session_state['selected_product'] = ""

    # Check if payment details should be shown
    # if st.session_state['show_payment_details']:
    #     show_payment_details()
    if st.session_state['show_policy_details']:
        show_policy_details()
    elif st.session_state['show_payment_details']:
        show_payment_details()
    else:
        index = 0
        while index < len(products):
            cols = st.columns(2)
            for col in cols:
                if index < len(products):
                    product = products[index]
                    with col:
                        col.markdown(f"""
                            <div style="padding:10px; margin:10px; border-radius:10px; border: 1px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,.1);">
                                <h4>{product['name']}</h4>
                                <p>{product['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                        if col.button("Buy / Renew", key=f"buy_{index}"):
                            handle_buy(product['name'], product['id'])
                            st.rerun()
                    index += 1
        # Form for adding new products
        if st.session_state['role'] == 'admin':
            st.header("Add New Product")
            product_name = st.text_input("Product Name")
            description = st.text_area("Description")
            coverage_desc = st.text_area("Coverage Description")
            if st.button("➕Add Product"):
                add_product(product_name, description, coverage_desc)