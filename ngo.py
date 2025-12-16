import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="NGO Website", layout="wide")

# ---------------- SESSION STATE ----------------
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

# ---------------- UI STYLING ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2c3e50;
}

.section {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Home Page", "Admin Dashboard"]
)

# ---------------- HOME PAGE ----------------
if menu == "Home Page":
    st.markdown('<div class="title">NGO Website</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Vision & Mission")
    st.write("**Vision:**", st.session_state.vision)
    st.write("**Mission:**", st.session_state.mission)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Our Statistics")
    col1, col2, col3 = st.columns(3)
    for col, stat in zip([col1, col2, col3], st.session_state.stats):
        col.metric(stat[0], stat[1])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Our Initiatives")
    for i in st.session_state.initiatives:
        st.write("•", i)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("📧 Contact: ngo@email.com")

# ---------------- ADMIN DASHBOARD ----------------
elif menu == "Admin Dashboard":
    st.markdown('<div class="title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Update Vision & Mission")
    vision = st.text_area("Vision", st.session_state.vision)
    mission = st.text_area("Mission", st.session_state.mission)

    if st.button("Save Vision & Mission"):
        st.session_state.vision = vision
        st.session_state.mission = mission
        st.success("Vision & Mission updated successfully")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Add Statistics")
    label = st.text_input("Statistic Label")
    value = st.text_input("Statistic Value")

    if st.button("Add Statistic"):
        if label and value:
            st.session_state.stats.append((label, value))
            st.success("Statistic added")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Add Initiative")
    init = st.text_input("Initiative Name")

    if st.button("Add Initiative"):
        if init:
            st.session_state.initiatives.append(init)
            st.success("Initiative added")
    st.markdown('</div>', unsafe_allow_html=True)