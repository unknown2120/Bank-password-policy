import streamlit as st

# --- SECURITY CONFIGURATION ---
USERNAME = "admin"
PASSWORD = "password123" # You can change this to your desired password

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# --- LOGIN LOGIC ---
def login():
    if st.session_state.username_input == USERNAME and st.session_state.password_input == PASSWORD:
        st.session_state.logged_in = True
        st.session_state.attempts = 0
    else:
        st.session_state.attempts += 1
        st.error(f"Wrong credentials! Attempt {st.session_state.attempts}/3")
        if st.session_state.attempts >= 3:
            st.error("Account BLOCKED. Please restart the app.")

# --- UI LAYER ---
if not st.session_state.logged_in:
    st.title("Bank Portal Login")
    
    if st.session_state.attempts < 3:
        st.text_input("Username", key="username_input")
        st.text_input("Password", type="password", key="password_input")
        st.button("Login", on_click=login)
    else:
        st.warning("Access Denied: Maximum attempts reached.")
    st.stop() # This prevents the rest of the app from showing

# --- PROTECTED DASHBOARD CONTENT ---
# Everything below this line only appears AFTER successful login
st.title("Bank Dashboard")
st.success("Successfully Logged In!")

st.write("### Policy Management System")
# Add your original dashboard code, charts, and policy logic here
st.write("You can now see the bank policy details and dashboard metrics.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
