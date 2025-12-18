import streamlit as st
import sqlite3
import os
from datetime import date

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="NGO Media Center",
    layout="wide",
    page_icon="📰"
)

# --------------------------------------------------
# ADMIN CREDENTIALS (Demo Only)
# --------------------------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
conn = sqlite3.connect("media.db", check_same_thread=False)
cur = conn.cursor()

# --------------------------------------------------
# DATABASE TABLES
# --------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS press_releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    release_date DATE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS media_coverage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS image_gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_url TEXT
)
""")

conn.commit()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio("", ["Media Page", "Admin Panel"])

# --------------------------------------------------
# ADMIN LOGIN (SIDEBAR)
# --------------------------------------------------
def admin_login():
    st.sidebar.subheader("🔐 Admin Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged = True
            st.sidebar.success("Login successful")
        else:
            st.sidebar.error("Invalid credentials")

# --------------------------------------------------
# MEDIA PAGE (FRONTEND)
# --------------------------------------------------
def media_page():
    st.title("🌍 NGO Media Center")
    st.markdown(
        "Stay updated with our **press releases, media mentions, photos, and videos** showcasing our impact."
    )

    st.divider()

    # ---------------- PRESS RELEASES ----------------
    st.header("📰 Press Releases")
    cur.execute("SELECT title, description, release_date FROM press_releases ORDER BY release_date DESC")
    releases = cur.fetchall()

    if releases:
        for pr in releases:
            with st.expander(pr[0]):
                st.write(pr[1])
                st.caption(f"📅 {pr[2]}")
    else:
        st.info("No press releases available.")

    # ---------------- MEDIA COVERAGE ----------------
    st.header("🌐 Media Coverage")
    cur.execute("SELECT title, url FROM media_coverage")
    media = cur.fetchall()

    if media:
        for m in media:
            st.markdown(f"🔗 **{m[0]}** — [Read Article]({m[1]})")
    else:
        st.info("No media coverage available.")

    # ---------------- IMAGE GALLERY ----------------
    st.header("🖼 Image Gallery")
    cur.execute("SELECT image_path FROM image_gallery")
    images = [i[0] for i in cur.fetchall()]

    if images:
        st.image(images, use_container_width=True)
    else:
        st.info("No images uploaded yet.")

    # ---------------- VIDEOS ----------------
    st.header("🎥 Videos")
    cur.execute("SELECT video_url FROM videos")
    videos = cur.fetchall()

    if videos:
        cols = st.columns(2)
        for i, v in enumerate(videos):
            cols[i % 2].video(v[0])
    else:
        st.info("No videos available.")

    st.divider()
    st.markdown("📩 **Media Contact:** media@ngo.org")

# --------------------------------------------------
# ADMIN PANEL
# --------------------------------------------------
def admin_panel():
    st.title("⚙ Admin Dashboard")

    tabs = st.tabs(["📰 Press", "🌐 Media", "🖼 Images", "🎥 Videos"])

    # -------- PRESS RELEASE --------
    with tabs[0]:
        st.subheader("Add Press Release")

        with st.form("press_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            release_date = st.date_input("Release Date", date.today())
            submitted = st.form_submit_button("Add")

        if submitted:
            cur.execute(
                "INSERT INTO press_releases VALUES (NULL, ?, ?, ?)",
                (title, description, release_date)
            )
            conn.commit()
            st.success("Press release added")

    # -------- MEDIA COVERAGE --------
    with tabs[1]:
        st.subheader("Add Media Coverage")

        title = st.text_input("Media Title")
        url = st.text_input("Article URL")

        if st.button("Add Media"):
            cur.execute(
                "INSERT INTO media_coverage VALUES (NULL, ?, ?)",
                (title, url)
            )
            conn.commit()
            st.success("Media added")

    # -------- IMAGE GALLERY --------
    with tabs[2]:
        st.subheader("Upload Image")

        image = st.file_uploader("Select Image", ["jpg", "png", "jpeg"])
        if image:
            os.makedirs("uploads/gallery", exist_ok=True)
            path = f"uploads/gallery/{image.name}"

            with open(path, "wb") as f:
                f.write(image.getbuffer())

            cur.execute("INSERT INTO image_gallery VALUES (NULL, ?)", (path,))
            conn.commit()
            st.success("Image uploaded")

    # -------- VIDEOS --------
    with tabs[3]:
        st.subheader("Add Video URL")

        video_url = st.text_input("YouTube / Video URL")
        if st.button("Add Video"):
            cur.execute("INSERT INTO videos VALUES (NULL, ?)", (video_url,))
            conn.commit()
            st.success("Video added")

# --------------------------------------------------
# MAIN LOGIC
# --------------------------------------------------
if menu == "Media Page":
    media_page()
else:
    if st.session_state.admin_logged:
        admin_panel()
    else:
        admin_login()
