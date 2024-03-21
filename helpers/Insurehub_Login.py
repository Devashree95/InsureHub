import streamlit as st
from helpers import connection as conn


connection = conn.pgsql_connect()
cur = connection.cursor()

def login_snippet(key="login"):
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    
    if "show_login" not in st.session_state:
        st.session_state.show_login = True  # By default, show the login form

    # Create an empty container for dynamic forms
    placeholder = st.empty()

    if not st.session_state.user_logged_in:
        if st.session_state.show_login:

            # Insert a form in the container
            with placeholder.form(key=key):
                st.markdown("#### Enter your credentials")
                email = st.text_input("Email")
                input_password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Log In")


            if submit:
                # If submit, check if the email exists in the database
                cur.execute("SELECT EXISTS (SELECT 1 FROM insurehub.users WHERE username = %s)", (email,))
                email_exists = cur.fetchone()
                if not email_exists[0]:
                    st.toast("Invalid username")
                    st.stop()

                # If submit, fetch password from the database
                cur.execute("SELECT password FROM insurehub.users WHERE username = %s", (email,))
                password = cur.fetchone()

                if input_password == password[0]:
                    st.toast("Login successful")
                    st.session_state.user_logged_in = True
                    if "username" not in st.session_state:
                        st.session_state.username = email
                    placeholder.empty()  # Clear the form
                    # You can redirect or continue execution here since the user is logged in
                    return True

                else:
                    st.toast("Login failed, incorrect password")
                    st.stop()
            
            create_account_button = st.button("Create new account")
            if create_account_button:
                st.session_state.show_login = False  # Hide login form and show account creation form
                placeholder.empty()  # Clear the existing form in the placeholder

        if not st.session_state.show_login:  # This means st.session_state.show_login is False, so show the account creation form
            with placeholder.form(key="create_account_form"):
                st.markdown("#### Enter your credentials to create a new account")
                new_email = st.text_input("Email", key="new_email")  # Use unique key for new form
                new_password = st.text_input("Password", type="password", key="new_password")  # Use unique key
                name = st.text_input("Name", key="name")
                submit_account = st.form_submit_button("Create Account")

            if submit_account:
                try:
                    print(new_email, new_password, name)
                    cur.execute("INSERT INTO insurehub.users (username, password, name) VALUES (%s, %s, %s)", (new_email, new_password, name))
                    connection.commit()
                    st.toast("Account created successfully")
                    placeholder.empty()
                    st.session_state.user_logged_in = True
                    return True
                    # st.session_state.show_login = True
                    # placeholder.empty()
                except Exception as e:
                    st.error(f"Error: {e}")
                    print(f"Error: {e}")
                    st.stop()
        
#             # Create new account button
#             create_account_button = st.button("Create new account")
#             if create_account_button:
#                 st.session_state.show_login = False  # Hide login form and show account creation form
#                 placeholder.empty()  # Clear the existing form in the placeholder
#                 st.session_state.show_login = create_account_snippet(key="create_account")


# def create_account_snippet(key="create_account"):
#     placeholder = st.empty()

#     with placeholder.form(key=key):
#         st.markdown("#### Enter your credentials to create a new account")
#         new_email = st.text_input("Email", key="new_email")  # Use unique key for new form
#         new_password = st.text_input("Password", type="password", key="new_password")  # Use unique key
#         name = st.text_input("Name", key="name")
#         submit_account = st.form_submit_button("Create Account")

#     if submit_account:
#         try:
#             print(new_email, new_password, name)
#             cur.execute("INSERT INTO insurehub.users (username, password, name) VALUES (%s, %s, %s)", (new_email, new_password, name))
#             connection.commit()
#             st.toast("Account created successfully")
#             st.session_state.show_login = True
#             return True
#         except Exception as e:
#             st.error(f"Error: {e}")
#             print(f"Error: {e}")
#             st.stop()
                
