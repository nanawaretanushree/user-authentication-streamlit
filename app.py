import streamlit as st

st.set_page_config(page_title="NGO Website", layout="wide")

# ---------- Session State ----------
if "vision" not in st.session_state:
    st.session_state.vision = "To uplift underprivileged communities."

if "mission" not in st.session_state:
    st.session_state.mission = "Provide education, healthcare, and support."

if "stats" not in st.session_state:
    st.session_state.stats = [
        ("Students Educated", "1000+"),
        ("Volunteers", "250+"),
        ("Campaigns", "50+")
    ]

if "initiatives" not in st.session_state:
    st.session_state.initiatives = [
        "Education for All",
        "Food Distribution",
        "Health Camps"
    ]

# ---------- Sidebar ----------
menu = st.sidebar.selectbox(
    "Menu",
    ["Home Page", "Admin Dashboard"]
)

# ---------- HOME PAGE ----------
if menu == "Home Page":
    st.title("NGO Website")

  
    st.header("Vision & Mission")
    st.write("**Vision:**", st.session_state.vision)
    st.write("**Mission:**", st.session_state.mission)

    st.header("Our Statistics")
    cols = st.columns(len(st.session_state.stats))
    for col, stat in zip(cols, st.session_state.stats):
        col.metric(stat[0], stat[1])

    st.header("Our Initiatives")
    for i in st.session_state.initiatives:
        st.write("•", i)

    st.write("---")
    st.write("📧 Contact: ngo@email.com")

# ---------- ADMIN DASHBOARD ----------
elif menu == "Admin Dashboard":
    st.title("Admin Dashboard")

    st.subheader("Update Vision & Mission")
    vision = st.text_area("Vision", st.session_state.vision)
    mission = st.text_area("Mission", st.session_state.mission)

    if st.button("Save Vision & Mission"):
        st.session_state.vision = vision
        st.session_state.mission = mission
        st.success("Vision & Mission updated")

    st.subheader("Add Statistics")
    label = st.text_input("Statistic Label")
    value = st.text_input("Statistic Value")

    if st.button("Add Statistic"):
        st.session_state.stats.append((label, value))
        st.success("Statistic added")

    st.subheader("Add Initiative")
    init = st.text_input("Initiative Name")

    if st.button("Add Initiative"):
        st.session_state.initiatives.append(init)
        st.success("Initiative added")