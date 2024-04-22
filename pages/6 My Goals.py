import streamlit as st
from PIL import Image
import base64
import uuid

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
    
    def get_user_name(email):
        query = f"SELECT name FROM insurehub.users_test WHERE username = '{email}'"
        cur.execute(query)
        custId = cur.fetchall()
        return custId[0][0]
    
    def get_agent_id(email):
        query = f"SELECT agent_id FROM insurehub.relationship_manager WHERE email = '{email}'"
        cur.execute(query)
        custId = cur.fetchall()
        return custId[0][0]

        
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

    #agent_id = '2A54EEDC-F811-129B-9A6C-D32E17EBAA0C'
    if st.session_state['role'] == 'agent':
        agent_id = get_agent_id(st.session_state['username'])
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

    def add_goal(name, rev, desc, date):
        query = f"INSERT INTO insurehub.goal VALUES ('{new_goal_id}', '{rev}', '{date}', 'Created', '{agent_id}', '{name}', '{desc}' )"
        cur.execute(query)
        connection.commit()

    def update_goal(goal_id, new_rev, new_date, new_status):
        query = f"UPDATE insurehub.goal SET tar_rev_per_mon = '{new_rev}', target_date = '{new_date}', status = '{new_status}' WHERE tar_rev_per_mon = '{goal_id}'"
        cur.execute(query)
        connection.commit()


    if st.session_state['role'] == 'agent':
        st.title("My Goals 🎯")
        name = get_user_name(st.session_state['username'])
		
        st.markdown(f"<h2 style='color: #ffffff;'>Welcome, {name}!</h2>", unsafe_allow_html=True)


        st.subheader("⚡Add a new goal:")
        # Add New Goal form
        with st.form("add_goal"):
            name= st.text_input("Goal Name")
            rev = st.text_input("Target Revenue")
            desc = st.text_input("Goal Description / Action Plan")
            date = st.date_input("Target Date")

            submit_button = st.form_submit_button("➕Add Goal")

            if submit_button:
                add_goal(name, rev, desc, date)
                st.success("Goal added successfully!🎉")
                st.experimental_rerun()
                
        st.subheader("⚡Manage Existing Goals")

        goals = fetch_goals()  # Fetch existing goals
        if goals:
            st.write("Goals:")
            for goal in goals:
                st.write(f"- {goal[1]}")  # Display goal name
            selected_goal_name = st.selectbox("Select a Goal to Manage", options=[goal[1] for goal in goals])
            selected_goal = next(goal for goal in goals if goal[1] == selected_goal_name)
            print(selected_goal_name)

            with st.form("goal_management"):
                new_rev = st.text_input("Target Revenue", value=str(selected_goal[1]))
                new_date = st.date_input("Target Date", value=selected_goal[2])
                new_status = st.selectbox("New Status", options=["In Progress", "Completed"], index=0 if selected_goal[4] == "In Progress" else 1)
                
                submit_button = st.form_submit_button("🖋️ Update Goal")
                if submit_button:
                    update_goal(selected_goal_name, new_rev, new_date, new_status)
                    st.success("Goal updated successfully! 🎉")
                    st.experimental_rerun()

        # Place the Delete button in a separate container to ensure it's not mistaken for a form submission action
        if goals and 'selected_goal_name' in locals():
            if st.button("🗑️ Delete Goal"):
                delete_goal(selected_goal_name)
                st.success("Goal deleted successfully! ✔️")
                st.experimental_rerun()
        else:
            st.write("No goals available to manage.")
 
    else:
        st.warning("You don't have access to this page.")