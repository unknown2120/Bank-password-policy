import streamlit as st
import json
import os
import time

USER_CREDENTIALS = {
    "infra_user": "Bank@Security1",
    "sys_user": "Bank@Security2",
    "db_user": "Bank@Security3",
    "standard_user": "Bank@Security4",
    "mgmt_user": "Bank@Security5",
    "third_user": "Bank@Security6",
    "network_user": "Bank@Security7"
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'lock_until' not in st.session_state:
    st.session_state.lock_until = 0

def login():
    input_user = st.session_state.username_input
    input_pwd = st.session_state.password_input
    if input_user in USER_CREDENTIALS and USER_CREDENTIALS[input_user] == input_pwd:
        st.session_state.logged_in = True
        st.session_state.role = input_user
        st.session_state.attempts = 0
        st.session_state.lock_until = 0
    else:
        st.session_state.attempts += 1
        if st.session_state.attempts >= 3:
            st.session_state.lock_until = time.time() + 300
            st.session_state.attempts = 0

if not st.session_state.logged_in:
    st.title("🏦 Bank Portal Login")
    if st.session_state.lock_until > 0 and time.time() < st.session_state.lock_until:
        remaining = int(st.session_state.lock_until - time.time())
        st.error(f"🔒 Account LOCKED. Try again in {remaining} seconds.")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.lock_until = 0
        st.text_input("Username", key="username_input")
        st.text_input("Password", type="password", key="password_input")
        st.button("Login", on_click=login)
        if st.session_state.attempts > 0:
            st.warning(f"⚠️ Wrong credentials! Attempt {st.session_state.attempts}/3")
    st.stop()

groups = [
    "Infrastructure Admins", "System Admins", "Database Admins",
    "Network Admins", "Standard Staff", "Management", "Third Party Vendors"
]

default_policies = {
    "Infrastructure Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "System Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Database Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Network Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Standard Staff": {"min_length": 12, "expiry_days": 90, "lockout_attempts": 5, "complexity": "Medium"},
    "Management": {"min_length": 14, "expiry_days": 60, "lockout_attempts": 5, "complexity": "High"},
    "Third Party Vendors": {"min_length": 14, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"}
}

policy_file = "policies.json"
if os.path.exists(policy_file):
    with open(policy_file, "r") as f:
        policies = json.load(f)
else:
    policies = default_policies

st.title("🏦 Bank Password Policy Management System")

col_title, col_logout = st.columns([8, 1])
with col_title:
    st.success(f"✅ Logged in as: {st.session_state.role}")
with col_logout:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.attempts = 0
        st.session_state.lock_until = 0
        st.rerun()

st.markdown("---")

st.sidebar.title("👤 Select User Group")
selected_group = st.sidebar.selectbox("Choose a group:", groups)

st.header(f"🔐 Password Policy for: {selected_group}")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Policy")
    current = policies[selected_group]
    st.info(f"🔑 Minimum Password Length: {current['min_length']} characters")
    st.info(f"📅 Password Expiry: {current['expiry_days']} days")
    st.info(f"🔒 Account Lockout After: {current['lockout_attempts']} failed attempts")
    st.info(f"⚡ Complexity Level: {current['complexity']}")

with col2:
    st.subheader("Update Policy")
    new_length = st.slider("Minimum Password Length", 8, 20, current["min_length"])
    new_expiry = st.slider("Password Expiry (days)", 30, 180, current["expiry_days"])
    new_lockout = st.slider("Lockout Attempts", 3, 10, current["lockout_attempts"])
    new_complexity = st.selectbox("Complexity Level", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(current["complexity"]))

    if st.button("💾 Save Policy"):
        policies[selected_group] = {
            "min_length": new_length,
            "expiry_days": new_expiry,
            "lockout_attempts": new_lockout,
            "complexity": new_complexity
        }
        with open(policy_file, "w") as f:
            json.dump(policies, f)
        st.success(f"✅ Policy for {selected_group} updated successfully!")

st.markdown("---")
st.header("📊 All Groups Policy Summary")
for group in groups:
    p = policies[group]
    st.write(f"**{group}** — Min Length: {p['min_length']} | Expiry: {p['expiry_days']} days | Lockout: {p['lockout_attempts']} attempts | Complexity: {p['complexity']}")
