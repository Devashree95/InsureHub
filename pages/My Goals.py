import streamlit as st
import helpers.sidebar
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from PIL import Image
import base64
import uuid
from datetime import datetime , timedelta


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
					<span style="padding:10px; flex:2;">Username</span>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)

agent_id = '2A54EEDC-F811-129B-9A6C-D32E17EBAA0C'
new_goal_id = str(uuid.uuid4()).upper()

def fetch_goals():
    query = f"SELECT * FROM insurehub.goal where agent_id = '{agent_id}'"  
    cur.execute(query)
    goals = cur.fetchall()
    return goals

def delete_goal(goal_id):
    query = f"Update insurehub.goal set status = 'Cancelled' WHERE goal_id = '{goal_id}' "  
    cur.execute(query)
    connection.commit()

def add_goal(rev, date):
    query = f"INSERT INTO insurehub.goal VALUES ('{new_goal_id}', '{rev}', '{date}', 'Created', '{agent_id}' )"
    cur.execute(query)
    connection.commit()

def update_goal(goal_id, new_rev, new_date):
    query = f"UPDATE insurehub.goal SET tar_rev_per_mon = '{new_rev}', target_date = '{new_date}' WHERE goal_id = '{goal_id}'"
    cur.execute(query)
    connection.commit()


st.title("My Goals 🎯")


st.subheader("Add a new goal:")
# Add New Goal form
with st.form("add_goal"):
    rev = st.text_input("Target Revenue")
    date = st.date_input("Target Date")

    submit_button = st.form_submit_button("Add Goal")

    if submit_button:
        add_goal(rev, date)
        st.success("Goal added successfully!")
        st.experimental_rerun()
        
st.subheader("Manage Existing Goals")

goals = fetch_goals()  # Fetch existing goals
if goals:
    goal_options = {f"Goal Id: {goal[0]} - Target Revenue: {goal[1]} - Target Date: {goal[2]} - Status: {goal[3]}": goal[0] for goal in goals}
    selected_goal_id = st.selectbox("Select a Goal to Manage", options=list(goal_options.keys()), format_func=lambda x: goal_options[x])
    print(selected_goal_id)
    with st.form("goal_management"):
        # Fields for updating a goal
        new_rev = st.text_input("Target Revenue", key="new_rev", value = selected_goal_id.split(" ")[6])
        new_date = st.text_input("Target Date", key="new_date", value = selected_goal_id.split(" ")[10])
        st.write(f"Status:  {selected_goal_id.split(' ')[13]}")
        
        # Action buttons
        update_button = st.form_submit_button("Update Goal")
        delete_button = st.form_submit_button("Delete Goal")
    
    if update_button:
        # Update goal logic
        update_goal(selected_goal_id.split(" ")[2], new_rev, new_date)
        st.success("Goal updated successfully!")
        st.experimental_rerun()
    
    if delete_button:
        # Delete goal logic
        delete_goal(selected_goal_id.split(" ")[2])
        st.success("Goal deleted successfully!")
        st.experimental_rerun()
else:
    st.write("No goals available to manage.")