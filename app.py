import streamlit as st

# --- OFFICIAL BANK ROLES ---
USER_CREDENTIALS = {
    "infra_user": "Bank@Security1",
    "sys_user": "Bank@Security2",
    "db_user": "Bank@Security3",
    "standard_user": "Bank@Security4",
    "mgmt_user": "Bank@Security5",
    "third_user": "Bank@Security6",
    "network_user": "Bank@Network7"
}

# --- INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

def login():
    input_user = st.session_state.username_input
    input_pwd = st.session_state.password_input
    
    # Check against the OFFICIAL list
    if input_user in USER_CREDENTIALS and USER_CREDENTIALS[input_user] == input_pwd:
        st.session_state.logged_in = True
        st.session_state.role = input_user
        st.session_state.attempts = 0
    else:
        st.session_state.attempts += 1
        st.error(f"Wrong credentials! Attempt {st.session_state.attempts}/3")

# --- LOGIN UI ---
if not st.session_state.logged_in:
    st.title("Bank Portal Login")
    if st.session_state.attempts < 3:
        st.text_input("Username", key="username_input")
        st.text_input("Password", type="password", key="password_input")
        st.button("Login", on_click=login)
    else:
        st.error("Account BLOCKED. Please restart.")
    st.stop()

# --- PROTECTED DASHBOARD ---
st.title("Bank Password Policy Management System")
st.success(f"Successfully logged in as: {st.session_state.role}")
st.write("You now have access to the Policy Management features.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
