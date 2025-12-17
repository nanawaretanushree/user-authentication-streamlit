import streamlit as st
import sqlite3

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    return sqlite3.connect("aboutus_v4.db", check_same_thread=False)

conn = connect_db()
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS story_tbl (content TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS values_tbl (value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS programs_tbl (program TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS team_tbl (name TEXT, role TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS impact_tbl (impact TEXT)")
conn.commit()

# ---------------- DEFAULT DATA ----------------
def seed_data():
    if cur.execute("SELECT COUNT(*) FROM story_tbl").fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO story_tbl VALUES ('Our NGO was established to serve society through meaningful initiatives.')"
        )

    if cur.execute("SELECT COUNT(*) FROM values_tbl").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO values_tbl VALUES (?)",
            [("Integrity",), ("Compassion",), ("Inclusiveness",)]
        )

    if cur.execute("SELECT COUNT(*) FROM programs_tbl").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO programs_tbl VALUES (?)",
            [("Education Support",), ("Health Camps",), ("Women Empowerment",)]
        )

    if cur.execute("SELECT COUNT(*) FROM team_tbl").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO team_tbl VALUES (?, ?)",
            [("Rohit Patil", "Founder"), ("Sneha Joshi", "Coordinator")]
        )

    if cur.execute("SELECT COUNT(*) FROM impact_tbl").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO impact_tbl VALUES (?)",
            [("4,000+ beneficiaries",), ("35+ programs executed",)]
        )

    conn.commit()

seed_data()

# ---------------- SESSION ----------------
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("About Us System")
page = st.sidebar.selectbox("Select Page", ["About Us", "Admin Panel"])

# ---------------- ABOUT US PAGE ----------------
if page == "About Us":
    st.title("About Our Organization")
    st.caption("Committed to social responsibility and community upliftment")

    with st.expander("📌 Mission & Vision", expanded=True):
        st.write("**Mission:** Empower communities through education and healthcare.")
        st.write("**Vision:** A society with equal opportunities for all.")

    with st.expander("📖 Our Story"):
        st.write(cur.execute("SELECT content FROM story_tbl").fetchone()[0])

    with st.expander("⭐ Core Values"):
        for v in cur.execute("SELECT value FROM values_tbl"):
            st.write(f"- {v[0]}")

    with st.expander("🛠 Programs"):
        for p in cur.execute("SELECT program FROM programs_tbl"):
            st.write(f"- {p[0]}")

    with st.expander("👥 Team"):
        for t in cur.execute("SELECT name, role FROM team_tbl"):
            st.write(f"**{t[0]}** – {t[1]}")

    with st.expander("📊 Impact"):
        for i in cur.execute("SELECT impact FROM impact_tbl"):
            st.write(f"- {i[0]}")

    st.success("Join us to make a positive change")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Donate")
    with col2:
        st.button("Volunteer")

# ---------------- ADMIN PANEL ----------------
elif page == "Admin Panel":
    if not st.session_state.admin_logged:
        st.subheader("Admin Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user == "admin" and pwd == "admin@123":
                st.session_state.admin_logged = True
                st.success("Login successful")
            else:
                st.error("Invalid login details")

    if st.session_state.admin_logged:
        st.subheader("Admin Dashboard")

        # Story
        st.markdown("### Edit Story")
        new_story = st.text_area(
            "Story Content",
            cur.execute("SELECT content FROM story_tbl").fetchone()[0]
        )
        if st.button("Save Story"):
            cur.execute("DELETE FROM story_tbl")
            cur.execute("INSERT INTO story_tbl VALUES (?)", (new_story,))
            conn.commit()
            st.success("Story updated")

        # Core Values
        st.markdown("### Add Core Value")
        new_val = st.text_input("Value")
        if st.button("Add Value"):
            cur.execute("INSERT INTO values_tbl VALUES (?)", (new_val,))
            conn.commit()

        # Programs
        st.markdown("### Add Program")
        new_prog = st.text_input("Program Name")
        if st.button("Add Program"):
            cur.execute("INSERT INTO programs_tbl VALUES (?)", (new_prog,))
            conn.commit()

        # Team
        st.markdown("### Add Team Member")
        name = st.text_input("Member Name")
        role = st.text_input("Member Role")
        if st.button("Add Member"):
            cur.execute("INSERT INTO team_tbl VALUES (?, ?)", (name, role))
            conn.commit()

        st.success("All changes saved successfully")