import streamlit as st
import helpers.sidebar
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from PIL import Image
import base64

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
    
def getPolicyDetails(custId):
    cur.execute(f"select pl.* from insurehub.policy pl join insurehub.purchases pur on pl.policy_id = pur.policy_id where cust_id = '{custId}'")
    
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return rows, columns
    
	
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


st.title('Welcome to Insurehub!')

st.write('Here are your policies:')

custId = '3E6BA8C7-DCA6-7296-2DD1-729B1B1731D6'

rows, columns = getPolicyDetails(custId)

df = pd.DataFrame(rows, columns=columns)
columns = ['policy_id','start_date', 'end_date', 'tot_coverage_amt' ]
df = df[columns]

# Rename columns
df = df.rename(columns={'policy_id': 'POLICY ID', 'start_date': 'START DATE', 'end_date': 'END DATE', 'tot_coverage_amt': 'Coverage Amount'})

st.dataframe(df)