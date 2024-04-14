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

    st.markdown("<h2>Welcome to InsureHub</h2>", unsafe_allow_html=True)
    # Define the content of the section
    section = "./images/insure.webp"
    image = Image.open(section)
    image_section = get_image_as_base64(section)
    st.markdown(f"""
    <div style="border: 2px solid #ccc; padding: 20px; display: flex; align-items: center;">
        <div style="flex: 1;">
            <h1 style="font-size: 36px; margin-bottom: 10px;">Fast way to get insured</h1>
            <ul>
                <li>Submit request online 24/7</li>
                <li>Fast and intuitive process</li>
                <li>Quality and real quotes</li>
               <button onclick="location.href='/buy-renew';" style="margin:15px; cursor: pointer; background-color: transparent; border: 2px solid white; color: white; padding: 5px 10px;">Buy / Renew</button>
            </ul>
        </div>
        <div style="flex: 1; text-align: center;">
            <img src="{image_section}" alt="Insurance Image" style="max-width: 100%; height: auto;">
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)


    # Define function to extract video ID from URL
    def extract_video_id(url):
        return url.split("?v=")[-1]

    # Display sections with YouTube videos side by side
    st.markdown('<div style="display: flex;">', unsafe_allow_html=True)
    st.markdown(f"""
        <div  style="display :flex; justify-content:center;">
            <div style="flex: 1; margin-right: 15px;">
               <iframe width="700" height="400" src="https://www.youtube.com/embed/3ctoSEQsY54" title="How Does Insurance Work?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    
    # Insurance Icons
    st.markdown("<h3>Our Insurance Services</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; justify-content: center;">
            <div style="margin: 30px;"> 
            <i class="fa-solid fa-car-burst fa-3x style="color: #66CC66;"></i>
                <p>AutoSecure</p>
            </div>
            <div style="margin: 30px;">
                <i class="fas fa-home fa-3x style="color: #66CC66;"></i>
                <p>HomeSafe</p>
            </div>
            <div style="margin: 30px;">
                <i class="fas fa-medkit fa-3x" style="color: #66CC66;"></i>
                <p>Health</p>
            </div>
            <div style="margin: 30px;">
                <i class="fa-solid fa-shield-dog fa-3x" style="color: #66CC66;"></i>
                <p>PetCare</p>
            </div>
           
            
        </div>
    """, unsafe_allow_html=True)

        # Contact Us Section
    st.markdown("<h3>Contact Us</h3>", unsafe_allow_html=True)
    st.markdown("""
        <p>Email: info@insurehub.com</p>
        <p>Phone: 123-456-7890</p>
        <!-- Add more contact details if necessary -->
    """, unsafe_allow_html=True)