import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import base64
import uuid

from helpers import connection as conn
from io import BytesIO


connection = conn.pgsql_connect()
cur = connection.cursor()


logo = "./images/profile_3135715.png"
image = Image.open(logo)

# if 'role' not in st.session_state:
#     st.session_state['role'] = "agent"

print(st.session_state['role'])

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
    
def getClaimDetails(policy_id):
    cur.execute(f"select * from insurehub.claim where policy_id = '{policy_id}'")
    
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return rows, columns

def select_claim(claim_id):
    st.session_state.selected_claim = claim_id

def getSingleClaimDetails(claim_id):
    query = f"SELECT * FROM insurehub.claim WHERE claim_id = '{claim_id}'"
    cur.execute(query)
    policy_details = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    if policy_details:
        return policy_details[0], columns  
    return None, None

def show_claim_details(claim_id):
    count = 0
    details, columns = getSingleClaimDetails(claim_id)
    if details:
        st.write(f"Details for Claim ID: {claim_id}")
        for col, val in zip(columns, details):
            #st.text(f"{col}: {val}")
            st.markdown(f"""
                <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                 	🔶 {col} : {val}
                </div>
            """, unsafe_allow_html=True)

        st.write("### Files")
        files = get_files_for_claim(claim_id)
        if files:
            for file_id, file_name in files:
                file_name, file_data = serve_file(file_id)
                if file_data:
                    col1, col2 = st.columns([3, 1])
                    file_container = f"""
                <div style="border: 2px solid #4CAF50; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(76, 175, 80, 0.1);">
                    <span style="font-size: 16px; font-weight: bold;">{file_name}</span><br>
                </div>
                """
                    with col1:
                        st.markdown(file_container, unsafe_allow_html=True)
                    with col2:
                        st.write('')
                        st.download_button(label=f"Download {file_name}",
                                   data=file_data,
                                   file_name=file_name,
                                   mime="application/octet-stream",  
                                   key=file_id)
        else:
            st.write("No files available for this claim.")
    else:
        st.error("Policy details could not be found.")

def approve_claim(claim_id):
    query = f"""
        update insurehub.claim set status = 'settled' where claim_id = '{claim_id}';
        """
    cur.execute(query)
    connection.commit()

    updated_at = datetime.now().date()
    query = f"""
        update insurehub.claim set claim_sett_dt = '{updated_at}' where claim_id = '{claim_id}';
        """
    cur.execute(query)
    connection.commit()

def reject_claim(claim_id):
    query = f"""
        update insurehub.claim set status = 'cancelled' where claim_id = '{claim_id}';
        """
    cur.execute(query)
    connection.commit()

    query = f"""
        update insurehub.claim set claim_sett_dt = NULL where claim_id = '{claim_id}';
        """
    cur.execute(query)
    connection.commit()

def agent_show_claim_details(claim_id):
    count = 0
    details, columns = getSingleClaimDetails(claim_id)
    if details:
        st.write(f"Details for Claim ID: {claim_id}")
        for col, val in zip(columns, details):
            #st.text(f"{col}: {val}")
            st.markdown(f"""
                <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                 	🔶 {col} : {val}
                </div>
            """, unsafe_allow_html=True)

        st.write("### Files")
        files = get_files_for_claim(claim_id)
        if files:
            for file_id, file_name in files:
                file_name, file_data = serve_file(file_id)
                if file_data:
                    col1, col2 = st.columns([3, 1])
                    file_container = f"""
                <div style="border: 2px solid #4CAF50; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(76, 175, 80, 0.1);">
                    <span style="font-size: 16px; font-weight: bold;">{file_name}</span><br>
                </div>
                """
                    with col1:
                        st.markdown(file_container, unsafe_allow_html=True)
                    with col2:
                        st.write('')
                        st.download_button(label=f"Download {file_name}",
                                   data=file_data,
                                   file_name=file_name,
                                   mime="application/octet-stream",  
                                   key=file_id)
        else:
            st.write("No files available for this claim.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Approve Claim', key=f'approve_{claim_id}'):
                approve_claim(claim_id)
                st.success('Claim Approved')
                # Optionally, rerun to refresh the data
                st.rerun()

        with col2:
            if st.button('Reject Claim', key=f'reject_{claim_id}'):
                reject_claim(claim_id) 
                st.error('Claim Rejected')
                # Optionally, rerun to refresh the data
                st.rerun()
    else:
        st.error("Policy details could not be found.")


def insert_new_claim(policy_id, claim_amount, date_filed, supporting_files):
    try:
        # Convert the date_filed to the appropriate format if needed, e.g., date_filed.strftime('%Y-%m-%d')
        # Assuming your table name is 'claim' and column names match the parameters
        claim_id = str(uuid.uuid4())

        query = f"""
        INSERT INTO insurehub.claim
        VALUES ('{claim_id}', '{claim_amount}', 'pending', '{date_filed}', NULL, '{policy_id}');
        """
        cur.execute(query)
        connection.commit()

        file_id = str(uuid.uuid4())
        
        # Handle supporting_files upload logic here
        for uploaded_file in supporting_files:
            # Read the contents of the uploaded file
            file_contents = uploaded_file.read()
            file_name = uploaded_file.name
            updated_at = datetime.now().date()
            
            # Insert file data into the database
            insert_file_query = """
            INSERT INTO insurehub.claim_files (claim_id, file_name, file_data, uploaded_at)
            VALUES (%s, %s, %s, %s);
            """
            # Use a parameterized query to safely insert the data
            try:
                cur.execute(insert_file_query, (claim_id, file_name, file_contents, updated_at))
                connection.commit()
            except Exception as e:
                print(f'Error while loading file to the files table: {e}')
                connection.rollback()  # Rollback in case of error
                
        connection.commit()

        st.success("Claim filed successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        connection.rollback()

def file_claim_form():
    with st.form("new_claim_form"):
        st.write("## File a New Claim")
        
        # Example fields for the form
        policy_id = st.text_input("Policy ID", max_chars=36)
        claim_amount = st.number_input("Claim Amount", min_value=0.01)
        date_filed = st.date_input("Date Filed", datetime.now())
        supporting_files = st.file_uploader("Upload Supporting Files", accept_multiple_files=True)
        
        submit_button = st.form_submit_button("Submit Claim")

        if submit_button:
            insert_new_claim(policy_id,claim_amount,date_filed,supporting_files)
        
    if not submit_button:
        if st.button("Back"):
            st.session_state['file_claim'] = False
            st.rerun()



def get_files_for_claim(claim_id):
    query = "SELECT file_id, file_name FROM insurehub.claim_files WHERE claim_id = %s;"
    cur.execute(query, (claim_id,))
    files = cur.fetchall()
    return files

def serve_file(file_id):
    # Fetch the file's binary data and name based on file_id
    query = "SELECT file_name, file_data FROM insurehub.claim_files WHERE file_id = %s;"
    cur.execute(query, (file_id,))
    file = cur.fetchone()
    if file:
        file_name, file_data = file
        return file_name, BytesIO(file_data)
    return None, None

def getStatus(claim_id):
    query = f"SELECT status FROM insurehub.claim WHERE claim_id = '{claim_id}'"
    cur.execute(query)
    status = cur.fetchall()
    return status[0][0]

def getDate(claim_id):
    query = f"SELECT claim_sett_dt FROM insurehub.claim WHERE claim_id = '{claim_id}'"
    cur.execute(query)
    end_date = cur.fetchall()
    return end_date[0][0]

def getPolicyId(email):
    if st.session_state['role'] == 'customer':
        query = f"select policy_id from insurehub.purchases pur join insurehub.customer cust on cust.cust_id = pur.cust_id where email = '{email}'"
    else:
        query = f"""select policy_id from insurehub.purchases pur 
                    join insurehub.customer cust 
                    on cust.cust_id = pur.cust_id 
                    join insurehub.relationship_manager rm
                    on cust.agent_id = rm.agent_id
                    where rm.email = '{email}'"""
    cur.execute(query)
    policy_ids = cur.fetchall()
    return policy_ids

	
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

if st.session_state['role'] == 'customer':
    st.title('My Claims:')

    # st.write('Here are your policies:')

    #policy_id = '7DB4D960-8AB5-7876-3B35-3465E625672D'
    policy_ids = getPolicyId(st.session_state['username'])
    list_of_policy_ids = [item[0] for item in policy_ids]

    if 'selected_claim' not in st.session_state:
        st.session_state.selected_claim = None

    if 'file_claim' in st.session_state and st.session_state['file_claim']:
        file_claim_form()
    else:
        if st.session_state['selected_claim']:
            show_claim_details(st.session_state.selected_claim)
            
            if st.button("Back to Claims List", key=f"back_to_list_{st.session_state['selected_claim']}"):
                st.session_state.selected_claim = None
                st.rerun()
        else:
            with st.container():
                for policy_id in list_of_policy_ids:
                    print(policy_id)
                    rows, columns = getClaimDetails(policy_id)
                    df = pd.DataFrame(rows, columns=columns)
                    columns = ['claim_id', 'claim_amount', 'status', 'date_filed', 'claim_sett_dt', 'policy_id']
                    df = df[columns]
                    df = df.rename(columns={'claim_id': 'CLAIM ID', 'claim_amount': 'CLAIM AMOUNT', 'status': 'STATUS', 'date_filed': 'DATE FILED', 'claim_sett_dt': 'CLAIM SETTLEMENT DATE' ,'policy_id': 'POLICY ID' })
                    
                    # Display policies with buttons to select for more details
                    for claim_id in df['CLAIM ID']:
                        st.markdown(f"""
                            <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                                💠 Claim ID: {claim_id} <br>
                                🔸 Status : {df['STATUS'].iloc[0]} <br>
                                🔸 Settled On: {df['CLAIM SETTLEMENT DATE'].iloc[0]}
                            </div>
                        """, unsafe_allow_html=True)

                        st.button(f"View Details", key=claim_id, on_click=select_claim, args=(claim_id,))

    if 'selected_claim' not in st.session_state or st.session_state['selected_claim'] is None:
        if 'file_claim' not in st.session_state or not st.session_state['file_claim']:
            st.header('Want to file a new claim?')
            st.write('Please fill out the following form to file new claim.')
            st.write('Make sure to have supporting documents ready.')
            if st.button('File a New Claim'):
                st.session_state['file_claim'] = True

elif st.session_state['role'] == 'agent':
    st.header("Manage Claims")

    # st.write('Here are your policies:')

    #policy_id = '7DB4D960-8AB5-7876-3B35-3465E625672D'
    policy_ids = getPolicyId(st.session_state['username'])
    list_of_policy_ids = [item[0] for item in policy_ids]

    if 'selected_claim' not in st.session_state:
        st.session_state.selected_claim = None

    if 'file_claim' in st.session_state and st.session_state['file_claim']:
        file_claim_form()
    else:
        if st.session_state['selected_claim']:
            agent_show_claim_details(st.session_state.selected_claim)
            
            if st.button("Back to Claims List", key=f"back_to_list_{st.session_state['selected_claim']}"):
                st.session_state.selected_claim = None
                st.rerun()
        else:
            with st.container():
                for policy_id in list_of_policy_ids:
                    rows, columns = getClaimDetails(policy_id)
                    df = pd.DataFrame(rows, columns=columns)
                    columns = ['claim_id', 'claim_amount', 'status', 'date_filed', 'claim_sett_dt', 'policy_id']
                    df = df[columns]
                    df = df.rename(columns={'claim_id': 'CLAIM ID', 'claim_amount': 'CLAIM AMOUNT', 'status': 'STATUS', 'date_filed': 'DATE FILED', 'claim_sett_dt': 'CLAIM SETTLEMENT DATE' ,'policy_id': 'POLICY ID' })
                    
                    # Display policies with buttons to select for more details
                    for claim_id in df['CLAIM ID']:
                        #st.write(f"Policy ID: {policy_id}")
                        st.markdown(f"""
                            <div style="border: 1px solid #ccc; margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(128, 128, 128, 0.1);">
                                💠 Claim ID: {claim_id} <br>
                                🔸 Status : {getStatus(claim_id)} <br>
                                🔸 Settled On: {getDate(claim_id)}
                            </div>
                        """, unsafe_allow_html=True)

                        st.button(f"View Details", key=claim_id, on_click=select_claim, args=(claim_id,))

else:
    st.warning('Nothing to show here.')
