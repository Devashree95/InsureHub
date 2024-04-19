import streamlit as st
import pandas as pd
from PIL import Image
import base64

from helpers import connection as conn


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
    
def getPolicyDetails(custId):
    cur.execute(f"select pl.* from insurehub.policy pl join insurehub.purchases pur on pl.policy_id = pur.policy_id where cust_id = '{custId}'")
    
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return rows, columns

def getSinglePolicyDetails(policy_id):
    query = f"SELECT * FROM insurehub.policy WHERE policy_id = '{policy_id}'"
    cur.execute(query)
    policy_details = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    if policy_details:
        return policy_details[0], columns  
    return None, None

def getStatus(policy_id):
    query = f"SELECT status FROM insurehub.policy WHERE policy_id = '{policy_id}'"
    cur.execute(query)
    status = cur.fetchall()
    return status[0][0]

def getRenewDate(policy_id):
    query = f"SELECT end_date FROM insurehub.policy WHERE policy_id = '{policy_id}'"
    cur.execute(query)
    end_date = cur.fetchall()
    return end_date[0][0]

def getCustId(email):
    query = f"SELECT cust_id FROM insurehub.customer WHERE email = '{email}'"
    cur.execute(query)
    custId = cur.fetchall()
    return custId[0][0]

def cancel_policy(policy_id):
    cancel_query = f"UPDATE insurehub.policy SET status = 'cancelled' WHERE policy_id = '{policy_id}'"
    cur.execute(cancel_query)
    connection.commit()
    pur_query = f"delete from insurehub.purchases where policy_id = '{policy_id}'"
    cur.execute(pur_query)
    connection.commit()
    
    st.success(f"Policy {policy_id} has been cancelled.")
    st.session_state.selected_policy = None 


def show_policy_details(policy_id):
    count = 0
    details, columns = getSinglePolicyDetails(policy_id)
    if details:
        st.write(f"Details for Policy ID: {policy_id}")
        for col, val in zip(columns, details):
            #st.text(f"{col}: {val}")
            st.markdown(f"""
                <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                 	🔶 {col} : {val}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Policy details could not be found.")

def back_to_list():
    st.session_state.selected_policy = None    
    
def select_policy(policy_id):
    st.session_state.selected_policy = policy_id

	
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


st.title('All Policies:')

# st.write('Here are your policies:')

#custId = '2DECA7C8-395E-5B44-4A3B-C792143C9F45'
custId = getCustId(st.session_state['username'])

if 'selected_policy' not in st.session_state:
    st.session_state.selected_policy = None

if st.session_state['selected_policy']:
    show_policy_details(st.session_state.selected_policy)
    if st.button("Cancel Policy", key=f"cancel_policy_{st.session_state['selected_policy']}"):
        cancel_policy(st.session_state['selected_policy'])
      
    # Button to go back to the policy list
    if st.button("Back to Policy List", key=f"back_to_list_{st.session_state['selected_policy']}"):
        st.session_state.selected_policy = None
else:
    st.subheader('Self policies:')
    # Assuming getPolicyDetails and the DataFrame setup are defined as before
    with st.container():
        rows, columns = getPolicyDetails(custId)
        df = pd.DataFrame(rows, columns=columns)
        columns = ['policy_id', 'start_date', 'end_date', 'tot_coverage_amt']
        df = df[columns]
        df = df.rename(columns={'policy_id': 'POLICY ID', 'start_date': 'START DATE', 'end_date': 'END DATE', 'tot_coverage_amt': 'Coverage Amount'})
        
        # Display policies with buttons to select for more details
        for policy_id in df['POLICY ID']:
            #st.write(f"Policy ID: {policy_id}")
            st.markdown(f"""
                <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                 💠 Policy ID: {policy_id} <br>
                 🔸 Status : {getStatus(policy_id)} <br>
                 🔸 Renewal Date: {getRenewDate(policy_id)} 
                </div>
            """, unsafe_allow_html=True)
            
            st.button(f"View Details", key=policy_id, on_click=select_policy, args=(policy_id,))