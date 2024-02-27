import streamlit as st
import helpers.sidebar
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from PIL import Image
import base64
import uuid

from helpers import connection as conn


helpers.sidebar.show()
connection = conn.pgsql_connect()
cur = connection.cursor()


logo = "./images/profile_3135715.png"
image = Image.open(logo)

# Function to convert image to Base64
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    
def getProductDetails():
    cur.execute(f"select product_name, description from insurehub.product")
    
    rows = cur.fetchall()
    products_list = [{"name": row[0], "description": row[1]} for row in rows]
    
    return products_list

def handle_buy(product_name):
    # Save the selected product name to the session state
    st.session_state['selected_product'] = product_name
    # Redirect to the payment details page
    st.session_state['show_payment_details'] = True

# Function to display payment details form and handle the transaction
def show_payment_details():
    st.write(f"You have chosen to buy: {st.session_state['selected_product']}")
    with st.form("payment_form", clear_on_submit=True):
        name_on_card = st.text_input("Name on Card")
        card_number = st.text_input("Card Number", max_chars=16)
        expiration_date = st.date_input("Expiration Date")
        cvv = st.text_input("CVV", max_chars=3)
        submit_button = st.form_submit_button("Pay")

        # if submit_button:
        #     st.success("Transaction was successful!")
        #     del st.session_state['selected_product']
        #     del st.session_state['show_payment_details']

        if submit_button:
            # Generate a unique policy ID
            policy_id = str(uuid.uuid4()).upper()
            
            # # Here, insert the new policy ID and other details into the policy table
            # try:
            #     cur.execute("INSERT INTO insurehub.policy (policy_id, product_name, ...) VALUES (%s, %s, ...)", 
            #                 (policy_id, st.session_state['selected_product'], ...))
            #     connection.commit()
            #     st.success("Transaction was successful! Your policy ID is: " + policy_id)
                
            #     # Clean up session state after successful transaction
            #     del st.session_state['selected_product']
            #     del st.session_state['show_payment_details']
            # except Exception as e:
            #     st.error("An error occurred while processing your transaction.")
            #     connection.rollback()



image_base64 = get_image_as_base64(logo)

st.markdown(f"""
			<a href="/" style="color:white;text-decoration: none;">
				<div style="display:table;margin-top:-15 rem;margin-left:0%; display: flex;">
			  		<img src="{image_base64}" alt="Insurehub Logo" style="width:50px;height:40px;margin-left:750px; flex:2;" </img>
					<span style="padding:10px; flex:2;">Username</span>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)


st.title('Explore our plans!')

products = getProductDetails()

if 'show_payment_details' not in st.session_state:
    st.session_state['show_payment_details'] = False

if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = ""

# Check if payment details should be shown
if st.session_state['show_payment_details']:
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
                        handle_buy(product['name'])
                index += 1