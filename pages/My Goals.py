import streamlit as st
import helpers.sidebar
import pandas as pd
import streamlit.components.v1 as components
from datetime import date 
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


st.title('My Goals!')

goal_operations = [("Add", "Add new goals"), ("Update", "Update your existing goal"), ("Delete", "Delete your existing goals")]


def generate_goal_id():
	
	if 'goal_id' not in st.session_state:
		
		st.session_state['goal_id'] = str(uuid.uuid4())


	return st.session_state['goal_id']

def get_agent_id():
	return "0381AA78-BF6A-8C7E-23B7-36728C8C43D5"

# Function to get goal operations
def get_goal_operations():
	return [{"name": operation[0], "description": operation[1]} for operation in goal_operations]

# Function to insert a new goal
# Function to insert a new goal
def insert_goal(goal_id, tar_rev_per_mon, target_date, status, agent_id):
	try:
		connection = conn.pgsql_connect()
		cursor = connection.cursor()

		query = f"""
		INSERT INTO insurehub.goal
		VALUES ('{goal_id}', '{tar_rev_per_mon}', '{target_date}', '{status}', '{agent_id}');
		"""

		# Print or log the SQL query for debugging
		print("Executing query:", query)

		# Execute the query and commit
		cursor.execute(query)
		connection.commit()

		# Query the database to verify if the goal has been added
		cursor.execute(f"SELECT * FROM insurehub.goal WHERE goal_id = '{goal_id}'")
		result = cursor.fetchone()

		if result:
			st.success("Goal added successfully!")
		else:
			st.error("Goal not added successfully. Please check for errors.")

	except Exception as e:
		st.error(f"An error occurred while processing your transaction: {e}")

	finally:
		cursor.close()
		connection.close()


# Function to update an existing goal
def update_goal(goal_id, tar_rev_per_mon, target_date, status, agent_id):
	try:
		connection = pgsql_connect()
		cursor = connection.cursor()

		# Example UPDATE query
		query = f"""
		UPDATE insurehub.goal
		SET tar_rev_per_mon = '{tar_rev_per_mon}',
			target_date = '{target_date}',
			status = '{status}',
			agent_id = '{agent_id}'
		WHERE goal_id = '{goal_id}';
		"""

		# Execute the query and commit
		cursor.execute(query)
		connection.commit()

		st.success("Goal updated successfully!")

	except Exception as e:
		st.error(f"An error occurred while processing your transaction: {e}")

	finally:
		cursor.close()
		connection.close()


# Function to delete an existing goal
def delete_goal(goal_id, agent_id):
	try:
		connection = pgsql_connect()
		cursor = connection.cursor()

		query = f"DELETE FROM insurehub.goal WHERE goal_id = '{goal_id}' AND agent_id = '{agent_id}';"


		cursor.execute(query)
		connection.commit()

		st.success("Goal deleted successfully!")

	except Exception as e:
		st.error(f"An error occurred while processing your transaction: {e}")

	finally:
		cursor.close()
		connection.close()


# Function to handle goal operations
def handle_goal_operation(operation_name):
	if operation_name == "Delete":
		show_delete_form()
	else:
		show_goal_form(operation_name)

# Function to display the goal form
# Function to display the goal form
def show_goal_form(operation_name):
	st.subheader(f"{operation_name} Goal")
	
	with st.form("goal_form"):
		goal_id_val = generate_goal_id()
		goal_id = st.text_input("Goal ID", value=goal_id_val, key="goal_id")
		tar_rev_per_mon = st.text_input("Target Revenue Per Month")
		target_date = st.date_input("Target Date", value=date.today())
		status = st.text_input("Status")
		agent_id = st.text_input("Agent ID", value=get_agent_id(), key="agent_id")

		# Customize submit button and functionality
		submit_button = st.form_submit_button(f" Goal")
		print(submit_button)

	# Check if form is submitted
	if submit_button:
		print("after click")
		if operation_name == "Add":
			print("insert")
			insert_goal(goal_id, tar_rev_per_mon, target_date, status, agent_id)
			st.success(f"Goal added successfully!")

		elif operation_name == "Update":
			update_goal(goal_id, tar_rev_per_mon, target_date, status, agent_id)
			st.success(f"Goal updated successfully!")

		elif operation_name == "Delete":
			delete_goal(goal_id, agent_id)
			st.success(f"Goal deleted successfully!")


# Function to display the delete form
def show_delete_form():
	st.subheader("Delete Goal")
	with st.form("delete_form"):
		goal_id_val = generate_goal_id()
		goal_id = st.text_input("Goal ID", value=goal_id_val, key="goal_id")
		agent_id = st.text_input("Agent ID", value=get_agent_id(), key="agent_id")

		# Customize submit button and functionality
		submit_button = st.form_submit_button("Delete Goal")

	# Handle form submission
	if submit_button:
		delete_goal(goal_id, agent_id)
		st.success(f"Goal deleted successfully!")


# Display goal operations
goal_operations_list = get_goal_operations()



index = 0
while index < len(goal_operations_list):
	cols = st.columns(2)
	for col in cols:
		if index < len(goal_operations_list):
			goal_operation = goal_operations_list[index]
			with col:
				col.markdown(f"""
					<div style="padding:10px; margin:10px; border-radius:10px; border: 1px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,.1);">
						<h4>{goal_operation['name']}</h4>
						<p>{goal_operation['description']}</p>
					</div>
					""", unsafe_allow_html=True)
				
				if col.button(f"{goal_operation['name']} Goal", key=f"{goal_operation['name'].lower()}_{index}"):
					handle_goal_operation(goal_operation['name'])
					print(goal_operation['name'])
			index += 1

