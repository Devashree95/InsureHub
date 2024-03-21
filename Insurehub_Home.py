import streamlit as st
import helpers.sidebar
from PIL import Image
import base64

from helpers.Insurehub_Login import login_snippet


st.set_page_config(
	page_title="InsureHub",
	page_icon="📄"
)

logo = "./images/profile_3135715.png"
image = Image.open(logo)


if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.toast("You need to login to access this page.")
    user_logged_in = login_snippet(key="buy_or_renew_login")


if st.session_state.user_logged_in:
    # Function to convert image to Base64
    def get_image_as_base64(path):
        with open(path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{data}"
        
    image_base64 = get_image_as_base64(logo)

    st.markdown(f"""
                <a href="/" style="color:white;text-decoration: none;">
                    <div style="display:table;margin-top:-15 rem;margin-left:0%; display: flex;">
                        <img src="{image_base64}" alt="PaperPalooza Logo" style="width:50px;height:40px;margin-left:750px; flex:2;" </img>
                        <span style="padding:10px; flex:2;">Username</span>
                    </div>
                </a>
                <br>
                    """, unsafe_allow_html=True)

    helpers.sidebar.show()

    st.markdown("Welcome to InsureHub!")

