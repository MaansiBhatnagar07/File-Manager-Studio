"""
📁 File Manager Studio
A polished Streamlit UI wrapping basic file operations: Create, Read, Update, Delete.

Run with:
    streamlit run file_manager_app.py
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------- PAGE CONFIG -----------------------------
LOGO_SVG = """
<svg width="0" height="0">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="50%" stop-color="#4f46e5"/>
      <stop offset="100%" stop-color="#0ea5e9"/>
    </linearGradient>
  </defs>
</svg>
"""

st.set_page_config(
    page_title="File Manager Studio",
    page_icon="🗂️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------- CUSTOM STYLES -----------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .main {
            padding-top: 1rem;
        }

        /* ---- Logo header ---- */
        .logo-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.7rem;
            margin-bottom: 0.3rem;
        }
        .logo-badge {
            width: 56px;
            height: 56px;
            border-radius: 16px;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #0ea5e9 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.35);
        }
        .logo-text {
            font-size: 1.9rem;
            font-weight: 700;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #0ea5e9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }

        /* ---- Buttons ---- */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            border: none;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #0ea5e9 100%);
            color: white;
            transition: 0.2s ease-in-out;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(79, 70, 229, 0.4);
        }

        /* Danger button variant (delete / overwrite confirm) */
        button[kind="secondary"] {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        }

        /* ---- Message boxes ---- */
        .success-box {
            padding: 0.9rem 1rem;
            border-radius: 10px;
            background-color: #ecfdf5;
            border-left: 5px solid #10b981;
            color: #065f46;
            margin-top: 0.7rem;
        }
        .error-box {
            padding: 0.9rem 1rem;
            border-radius: 10px;
            background-color: #fef2f2;
            border-left: 5px solid #ef4444;
            color: #991b1b;
            margin-top: 0.7rem;
        }
        .warn-box {
            padding: 0.9rem 1rem;
            border-radius: 10px;
            background-color: #fffbeb;
            border-left: 5px solid #f59e0b;
            color: #92400e;
            margin-top: 0.7rem;
        }
        .file-content {
            background-color: #0f172a;
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            margin-top: 0.7rem;
        }
        .meta-chip {
            display: inline-block;
            background-color: #eef2ff;
            color: #4338ca;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.78rem;
            margin-right: 0.4rem;
        }
        .card {
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            background: #ffffff0d;
            border: 1px solid rgba(120, 120, 150, 0.15);
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_logo():
    st.markdown(
        """
        <div class="logo-header">
            <div class="logo-badge">🗂️</div>
            <div class="logo-text">File Manager Studio</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------- HELPERS -----------------------------
def show_success(msg: str):
    st.markdown(f'<div class="success-box">✅ {msg}</div>', unsafe_allow_html=True)


def show_error(msg: str):
    st.markdown(f'<div class="error-box">❌ {msg}</div>', unsafe_allow_html=True)


def show_warn(msg: str):
    st.markdown(f'<div class="warn-box">⚠️ {msg}</div>', unsafe_allow_html=True)


def file_meta(path: Path) -> str:
    """Return a small HTML chip strip with file size + last modified time."""
    try:
        stat = path.stat()
        size_kb = stat.st_size / 1024
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        return (
            f'<span class="meta-chip">📦 {size_kb:.2f} KB</span>'
            f'<span class="meta-chip">🕒 {modified}</span>'
        )
    except Exception:
        return ""


def reset_confirmations():
    """Clear any pending confirmation flags when switching context/files."""
    for key in ["confirm_delete", "confirm_overwrite", "confirm_rename"]:
        st.session_state.pop(key, None)


# ----------------------------- SIDEBAR -----------------------------
st.sidebar.markdown("### 🗂️ File Manager Studio")
st.sidebar.caption("A simple CRUD tool for local files, built with Python & Streamlit.")
st.sidebar.markdown("---")

operation = st.sidebar.radio(
    "Choose an operation",
    ["🏠 Home", "📝 Create File", "📖 Read File", "🔧 Update File", "🗑️ Delete File"],
    on_change=reset_confirmations,
)

st.sidebar.markdown("---")
st.sidebar.caption(f"🕒 Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.caption("Made with ❤️ using `pathlib` + Streamlit")

# ----------------------------- HOME -----------------------------
if operation == "🏠 Home":
    show_logo()
    st.markdown('<p class="subtitle">Create, Read, Update & Delete files — all from one clean dashboard.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("**📝 Create**\n\nMake a new file and write initial content into it.")
        st.info("**🔧 Update**\n\nRename, append to, or overwrite an existing file — with confirmation.")
    with col2:
        st.info("**📖 Read**\n\nView the contents of any existing file, with size & timestamp.")
        st.info("**🗑️ Delete**\n\nRemove a file safely, with a confirm-before-delete step.")
    st.markdown("---")
    st.caption("Built with ❤️ using Python's `pathlib` and Streamlit.")

# ----------------------------- CREATE -----------------------------
elif operation == "📝 Create File":
    show_logo()
    st.subheader("📝 Create a New File")
    filename = st.text_input("File name (e.g. notes.txt)")
    content = st.text_area("What do you want to write?", height=180)

    if st.button("Create File"):
        if not filename.strip():
            show_error("Please enter a file name.")
        else:
            path = Path(filename)
            if path.exists():
                show_error(f"A file named **{filename}** already exists. Try a different name.")
            else:
                try:
                    path.write_text(content)
                    show_success(f"File **{filename}** created successfully!")
                    st.markdown(file_meta(path), unsafe_allow_html=True)
                except Exception as err:
                    show_error(f"Something went wrong: {err}")

# ----------------------------- READ -----------------------------
elif operation == "📖 Read File":
    show_logo()
    st.subheader("📖 Read a File")
    filename = st.text_input("File name to read")

    if st.button("Read File"):
        if not filename.strip():
            show_error("Please enter a file name.")
        else:
            path = Path(filename)
            if not path.exists():
                show_error(f"No file named **{filename}** was found.")
            else:
                try:
                    content = path.read_text()
                    show_success(f"Loaded **{filename}** successfully.")
                    st.markdown(file_meta(path), unsafe_allow_html=True)
                    st.markdown(f'<div class="file-content">{content or "(file is empty)"}</div>', unsafe_allow_html=True)
                except Exception as err:
                    show_error(f"Something went wrong: {err}")

# ----------------------------- UPDATE -----------------------------
elif operation == "🔧 Update File":
    show_logo()
    st.subheader("🔧 Update a File")
    filename = st.text_input("File name to update")
    action = st.selectbox("Choose an action", ["Rename file", "Append content", "Overwrite content"])

    # --- Rename ---
    if action == "Rename file":
        new_name = st.text_input("New file name")

        if st.button("Rename"):
            if not filename.strip() or not new_name.strip():
                show_error("Please fill in both file names.")
            elif not Path(filename).exists():
                show_error(f"No file named **{filename}** was found.")
            elif Path(new_name).exists():
                show_error(f"A file named **{new_name}** already exists.")
            else:
                st.session_state["confirm_rename"] = (filename, new_name)

        if st.session_state.get("confirm_rename"):
            old_n, new_n = st.session_state["confirm_rename"]
            show_warn(f"Rename **{old_n}** ➜ **{new_n}**? This cannot be undone automatically.")
            c1, c2 = st.columns(2)
            if c1.button("✅ Yes, rename it"):
                try:
                    Path(old_n).rename(Path(new_n))
                    show_success(f"Renamed **{old_n}** to **{new_n}** successfully!")
                except Exception as err:
                    show_error(f"Something went wrong: {err}")
                finally:
                    st.session_state.pop("confirm_rename", None)
            if c2.button("❌ Cancel"):
                st.session_state.pop("confirm_rename", None)
                show_warn("Rename cancelled.")

    # --- Append ---
    elif action == "Append content":
        data = st.text_area("Text to append", height=150)
        if st.button("Append"):
            if not filename.strip():
                show_error("Please enter a file name.")
            elif not Path(filename).exists():
                show_error(f"No file named **{filename}** was found.")
            else:
                try:
                    path = Path(filename)
                    with open(path, "a") as fs:
                        fs.write("\n" + data)
                    show_success(f"Content appended to **{filename}** successfully!")
                    st.markdown(file_meta(path), unsafe_allow_html=True)
                except Exception as err:
                    show_error(f"Something went wrong: {err}")

    # --- Overwrite ---
    elif action == "Overwrite content":
        data = st.text_area("New content (replaces existing content)", height=150)

        if st.button("Overwrite"):
            if not filename.strip():
                show_error("Please enter a file name.")
            elif not Path(filename).exists():
                show_error(f"No file named **{filename}** was found.")
            else:
                st.session_state["confirm_overwrite"] = (filename, data)

        if st.session_state.get("confirm_overwrite"):
            fname, new_data = st.session_state["confirm_overwrite"]
            show_warn(f"This will permanently replace all existing content in **{fname}**. Continue?")
            c1, c2 = st.columns(2)
            if c1.button("✅ Yes, overwrite it"):
                try:
                    Path(fname).write_text(new_data)
                    show_success(f"**{fname}** overwritten successfully!")
                    st.markdown(file_meta(Path(fname)), unsafe_allow_html=True)
                except Exception as err:
                    show_error(f"Something went wrong: {err}")
                finally:
                    st.session_state.pop("confirm_overwrite", None)
            if c2.button("❌ Cancel"):
                st.session_state.pop("confirm_overwrite", None)
                show_warn("Overwrite cancelled.")

# ----------------------------- DELETE -----------------------------
elif operation == "🗑️ Delete File":
    show_logo()
    st.subheader("🗑️ Delete a File")
    filename = st.text_input("File name to delete")

    if st.button("Delete File"):
        if not filename.strip():
            show_error("Please enter a file name.")
        elif not Path(filename).exists():
            show_error(f"No file named **{filename}** was found.")
        else:
            st.session_state["confirm_delete"] = filename

    if st.session_state.get("confirm_delete"):
        fname = st.session_state["confirm_delete"]
        show_warn(f"Are you sure you want to permanently delete **{fname}**? This cannot be undone.")
        c1, c2 = st.columns(2)
        if c1.button("✅ Yes, delete it"):
            try:
                Path(fname).unlink()
                show_success(f"**{fname}** deleted successfully!")
            except Exception as err:
                show_error(f"Something went wrong: {err}")
            finally:
                st.session_state.pop("confirm_delete", None)
        if c2.button("❌ Cancel"):
            st.session_state.pop("confirm_delete", None)
            show_warn("Deletion cancelled.")
