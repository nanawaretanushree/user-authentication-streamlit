import streamlit as st

st.set_page_config(page_title="User Authentication App", layout="centered")

# Title
st.markdown(
    "<h1 style='text-align:center;'>🔐 User Authentication App</h1>",
    unsafe_allow_html=True
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# Simple in-memory user storage
if "users" not in st.session_state:
    st.session_state.users = {"Tanushree": "1234"}

# Sidebar menu
if st.session_state.logged_in:
    menu = ["Dashboard"]
else:
    menu = ["Login", "Signup", "About"]

choice = st.sidebar.radio("Menu", menu)

# ---------------- LOGIN ----------------
if choice == "Login":
    st.markdown("### Login to your account")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# ---------------- SIGNUP ----------------
elif choice == "Signup":
    st.markdown("### Create a new account")

    new_user = st.text_input("👤 New Username")
    new_pass = st.text_input("🔑 New Password", type="password")

    if st.button("Signup"):
        if new_user == "" or new_pass == "":
            st.warning("⚠️ Please fill all fields")
        elif new_user in st.session_state.users:
            st.error("❌ Username already exists")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("🎉 Account created successfully")
            st.info("Now go to Login")

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard":
    st.success(f"Welcome, {st.session_state.user} 🌸")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

# ---------------- ABOUT ----------------
elif choice == "About":
    st.markdown("### 📘 About this project")
    st.info(
        """
        This is a **User Authentication App** built using **Python and Streamlit**.

        Features:
        - Signup & Login
        - Dashboard after login
        - Logout functionality
        - Clean UI

        This project is suitable for **internship / academic submission**.
        """
    )