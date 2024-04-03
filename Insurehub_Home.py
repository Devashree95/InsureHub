import streamlit as st
import helpers.sidebar
from PIL import Image
import base64
from st_pages import Page, show_pages

from helpers.Insurehub_Login import login_snippet


st.set_page_config(
	page_title="InsureHub",
	page_icon="📄",
    layout="wide"
)


col3, col1, col2 = st.columns([1,2, 1])

logo1 = "./images/logo.png"
image = Image.open(logo1)

def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{data}"

st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


logo = "./images/profile_3135715.png"
image = Image.open(logo)

image_base64 = get_image_as_base64(logo)

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

if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.toast("You need to login to access this page.")
    with col1:
        user_logged_in = login_snippet(key="buy_or_renew_login")


if st.session_state.user_logged_in:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)
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
                        <span style="padding:10px; flex:2;">{st.session_state['username']}</span>
                    </div>
                </a>
                <br>
                    """, unsafe_allow_html=True)

    helpers.sidebar.show()

    st.markdown("Welcome to InsureHub!")

