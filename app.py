import streamlit as st
import json
import os

st.set_page_config(page_title="Bank Password Policy Manager", layout="wide")

st.title("🏦 Bank Password Policy Management System")
st.markdown("---")

# Define 7 bank user groups
groups = [
    "Infrastructure Admins",
    "System Admins", 
    "Database Admins",
    "Network Admins",
    "Standard Staff",
    "Management",
    "Third Party Vendors"
]

# Default policies for each group
default_policies = {
    "Infrastructure Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "System Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Database Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Network Admins": {"min_length": 16, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"},
    "Standard Staff": {"min_length": 12, "expiry_days": 90, "lockout_attempts": 5, "complexity": "Medium"},
    "Management": {"min_length": 14, "expiry_days": 60, "lockout_attempts": 5, "complexity": "High"},
    "Third Party Vendors": {"min_length": 14, "expiry_days": 30, "lockout_attempts": 3, "complexity": "High"}
}

# Load saved policies
policy_file = "policies.json"
if os.path.exists(policy_file):
    with open(policy_file, "r") as f:
        policies = json.load(f)
else:
    policies = default_policies

# Sidebar - Select Group
st.sidebar.title("👤 Select User Group")
selected_group = st.sidebar.selectbox("Choose a group:", groups)

# Main area
st.header(f"📋 Password Policy for: {selected_group}")
st.markdown("---")

# Show current policy
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Policy")
    current = policies[selected_group]
    st.info(f"🔑 Minimum Password Length: **{current['min_length']} characters**")
    st.info(f"📅 Password Expiry: **{current['expiry_days']} days**")
    st.info(f"🔒 Account Lockout After: **{current['lockout_attempts']} failed attempts**")
    st.info(f"⚡ Complexity Level: **{current['complexity']}**")

with col2:
    st.subheader("Update Policy")
    new_length = st.slider("Minimum Password Length", 8, 20, current['min_length'])
    new_expiry = st.slider("Password Expiry (days)", 30, 180, current['expiry_days'])
    new_lockout = st.slider("Lockout Attempts", 3, 10, current['lockout_attempts'])
    new_complexity = st.selectbox("Complexity Level", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(current['complexity']))

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

# Show all groups summary
st.header("📊 All Groups Policy Summary")
for group in groups:
    p = policies[group]
    st.write(f"**{group}** — Min Length: {p['min_length']} | Expiry: {p['expiry_days']} days | Lockout: {p['lockout_attempts']} attempts | Complexity: {p['complexity']}")
