import streamlit as st
import sqlite3
import os
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NGO | Our Projects",
    page_icon="🌱",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; }
.project-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.project-title { font-size: 22px; font-weight: 700; }
.badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.ongoing { background:#e3f2fd; color:#1565c0; }
.completed { background:#e8f5e9; color:#2e7d32; }
.upcoming { background:#fff3e0; color:#ef6c00; }
.admin-box {
    background:white;
    padding:25px;
    border-radius:14px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SETUP ----------------
os.makedirs("uploads", exist_ok=True)

def db():
    return sqlite3.connect("projects.db", check_same_thread=False)

# ---------------- DATABASE ----------------
def setup():
    c = db()
    cur = c.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        status TEXT,
        start_date DATE,
        end_date DATE,
        location TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        path TEXT
    )
    """)
    c.commit()
    c.close()

setup()

# ---------------- SESSION ----------------
if "admin" not in st.session_state:
    st.session_state.admin = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 NGO Panel")
page = st.sidebar.radio("Navigate", ["Our Projects", "Admin Dashboard"])

# =================================================
# USER VIEW
# =================================================
if page == "Our Projects":
    st.markdown("## 🌱 Our Projects")

    filter_status = st.selectbox(
        "Filter by status",
        ["All", "Ongoing", "Completed", "Upcoming"]
    )

    c = db()
    cur = c.cursor()
    if filter_status == "All":
        cur.execute("SELECT * FROM projects")
    else:
        cur.execute("SELECT * FROM projects WHERE status=?", (filter_status,))
    projects = cur.fetchall()

    for p in projects:
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">{p[1]}</div>
            <span class="badge {p[3].lower()}">{p[3]}</span>
            <p>{p[2]}</p>
            <p>📍 <b>{p[6]}</b></p>
            <p>🗓 {p[4]} → {p[5]}</p>
        """, unsafe_allow_html=True)

        cur.execute("SELECT path FROM images WHERE project_id=?", (p[0],))
        img = cur.fetchone()
        if img and os.path.exists(img[0]):
            st.image(img[0], use_column_width=True)

        with st.expander("Learn More"):
            st.write("This project contributes to long-term social impact.")

        st.markdown("</div>", unsafe_allow_html=True)

    c.close()

    c1, c2, c3 = st.columns(3)
    c1.metric("People Helped", "500+")
    c2.metric("Volunteers", "300+")
    c3.metric("Funds Raised", "₹50,000+")

# =================================================
# ADMIN DASHBOARD
# =================================================
else:
    st.markdown("## 🔐 Admin Dashboard")

    # ---------- LOGIN ----------
    if not st.session_state.admin:
        st.markdown('<div class="admin-box">', unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u == "admin" and p == "admin123":
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # ---------- PROJECT LIST ----------
    c = db()
    cur = c.cursor()
    cur.execute("SELECT id, title FROM projects")
    plist = cur.fetchall()
    c.close()

    choice = st.selectbox("Select Project", ["New Project"] + [x[1] for x in plist])

    edit = None
    pid = None
    if choice != "New Project":
        pid = [x[0] for x in plist if x[1] == choice][0]
        c = db()
        cur = c.cursor()
        cur.execute("SELECT * FROM projects WHERE id=?", (pid,))
        edit = cur.fetchone()
        c.close()

    # ---------- FORM ----------
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)

    title = st.text_input("Project Title", edit[1] if edit else "")
    desc = st.text_area("Description", edit[2] if edit else "")
    status = st.selectbox(
        "Status",
        ["Ongoing", "Completed", "Upcoming"],
        index=["Ongoing", "Completed", "Upcoming"].index(edit[3]) if edit else 0
    )
    sd = st.date_input("Start Date", edit[4] if edit else date.today())
    ed = st.date_input("End Date", edit[5] if edit else date.today())
    loc = st.text_input("Location", edit[6] if edit else "")
    img = st.file_uploader("Project Image", type=["jpg", "png", "jpeg"])

    # ---------- SAVE PROJECT ----------
    if st.button("Save Project"):
        c = db()
        cur = c.cursor()

        if edit:
            cur.execute("""
                UPDATE projects
                SET title=?, description=?, status=?, start_date=?, end_date=?, location=?
                WHERE id=?
            """, (title, desc, status, sd, ed, loc, pid))
        else:
            cur.execute("""
                INSERT INTO projects VALUES (NULL,?,?,?,?,?,?)
            """, (title, desc, status, sd, ed, loc))
            pid = cur.lastrowid

        if img:
            img_path = f"uploads/{pid}_{img.name}"
            with open(img_path, "wb") as f:
                f.write(img.getbuffer())

            cur.execute("DELETE FROM images WHERE project_id=?", (pid,))
            cur.execute(
                "INSERT INTO images (project_id, path) VALUES (?,?)",
                (pid, img_path)
            )

        c.commit()
        c.close()
        st.success("Project saved successfully")
        st.rerun()

    # ---------- DELETE PROJECT ----------
    if edit:
        st.markdown("---")
        st.warning("Danger Zone")

        if st.button("🗑 Delete Project"):
            c = db()
            cur = c.cursor()

            cur.execute("SELECT path FROM images WHERE project_id=?", (pid,))
            img = cur.fetchone()
            if img and os.path.exists(img[0]):
                os.remove(img[0])

            cur.execute("DELETE FROM images WHERE project_id=?", (pid,))
            cur.execute("DELETE FROM projects WHERE id=?", (pid,))

            c.commit()
            c.close()

            st.success("Project deleted successfully")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)