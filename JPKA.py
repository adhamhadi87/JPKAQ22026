import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from textwrap import dedent
import os
import streamlit.components.v1 as components

# =======================
# TETAPAN PAGE
# =======================
st.set_page_config(
    page_title="PRESTASI PERBELANJAAN DAN HASIL CIDB SEHINGGA SUKU KEDUA 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =======================
# LOGIN / PASSWORD APP
# =======================
# Password utama:
# - Streamlit Cloud: letak APP_PASSWORD dalam Settings > Secrets
# - Local PC: kalau tiada secrets/env, default sementara ialah "JPKA062026"
#   Tukar default ini kalau mahu password lain.
DEFAULT_APP_PASSWORD = "JPKA062026"


def get_app_password():
    """Ambil password daripada st.secrets, environment, atau default."""
    password = ""

    try:
        password = str(st.secrets.get("APP_PASSWORD", "")).strip()
    except Exception:
        password = ""

    if not password:
        password = str(os.environ.get("APP_PASSWORD", "")).strip()

    if not password:
        password = DEFAULT_APP_PASSWORD

    return password


def require_login():
    """Papar login page dan stop app jika belum login."""
    if st.session_state.get("dashboard_authenticated", False):
        return

    st.markdown(
        """
        <div style="
            max-width: 460px;
            margin: 8vh auto 1rem auto;
            padding: 28px 30px;
            border-radius: 22px;
            background: rgba(255,255,255,0.78);
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 18px 45px rgba(15,23,42,0.16);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            text-align: center;
        ">
            <div style="font-size:42px; line-height:1; margin-bottom:8px;">🔐</div>
            <h2 style="margin:0; color:#1e293b; font-weight:800;">Login Dashboard</h2>
            <p style="margin:8px 0 0 0; color:#64748b; font-size:14px;">
                Masukkan password untuk akses Dashboard Prestasi Kewangan CIDB.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_dashboard_form", clear_on_submit=False):
        password_input = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password"
        )
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if password_input == get_app_password():
            st.session_state["dashboard_authenticated"] = True
            st.rerun()
        else:
            st.error("Password salah. Sila cuba semula.")

    st.stop()


require_login()


# =========================================================
# SIDEBAR PILLS - DARK GLASS STYLE
# Tulisan lebih jelas, transparent masih kekal.
# =========================================================
st.markdown("""
<style>

/* ================================
   SIDEBAR EXPANDER - DARK GLASS
================================ */

section[data-testid="stSidebar"] div[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.32) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 18px !important;
    box-shadow:
        0 10px 24px rgba(0,0,0,0.18),
        inset 0 1px 0 rgba(255,255,255,0.10) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    margin-bottom: 12px !important;
    overflow: hidden !important;
}

/* Header expander */
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 10px 12px !important;
}

/* Pastikan title/summary nampak */
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary,
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary *,
section[data-testid="stSidebar"] div[data-testid="stExpander"] p,
section[data-testid="stSidebar"] div[data-testid="stExpander"] span,
section[data-testid="stSidebar"] div[data-testid="stExpander"] label {
    color: #F8FAFC !important;
    opacity: 1 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.45);
    font-weight: 700 !important;
}

/* Caption dalam expander */
section[data-testid="stSidebar"] div[data-testid="stExpander"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] div[data-testid="stExpander"] [data-testid="stCaptionContainer"] * {
    color: #CBD5E1 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* ================================
   PILLS - DARK MIRROR
================================ */

/* Semua pill */
section[data-testid="stSidebar"] button[data-baseweb="tag"] {
    background: rgba(30, 41, 59, 0.62) !important;
    border: 1px solid rgba(255,255,255,0.24) !important;

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    border-radius: 999px !important;
    color: #F8FAFC !important;

    transition: all 0.20s ease;

    box-shadow:
        0 6px 18px rgba(0,0,0,0.22),
        inset 0 1px 1px rgba(255,255,255,0.14);

    padding: 0.25rem 0.85rem !important;
}

/* Text dalam pill */
section[data-testid="stSidebar"] button[data-baseweb="tag"] *,
section[data-testid="stSidebar"] button[data-baseweb="tag"] span,
section[data-testid="stSidebar"] button[data-baseweb="tag"] div {
    color: #F8FAFC !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.45);
}

/* Hover */
section[data-testid="stSidebar"] button[data-baseweb="tag"]:hover {
    background: rgba(51, 65, 85, 0.82) !important;
    border-color: rgba(255,255,255,0.40) !important;
    transform: translateY(-1px);
}

/* Selected pill */
section[data-testid="stSidebar"] button[data-baseweb="tag"][aria-pressed="true"] {
    background: linear-gradient(
        135deg,
        rgba(37, 99, 235, 0.90),
        rgba(14, 165, 233, 0.62)
    ) !important;

    border: 1px solid rgba(255,255,255,0.55) !important;
    color: #FFFFFF !important;

    box-shadow:
        0 8px 26px rgba(37,99,235,0.35),
        inset 0 1px 1px rgba(255,255,255,0.30);
}

/* ================================
   Sidebar background keep corporate
================================ */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(15,23,42,0.96) 0%,
            rgba(30,58,138,0.92) 55%,
            rgba(15,23,42,0.96) 100%
        ) !important;
}

/* General sidebar text */
section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

</style>
""", unsafe_allow_html=True)


def html(kod_html):
    st.markdown(dedent(kod_html).strip(), unsafe_allow_html=True)


html("""
<style>
/* Header, toolbar, Main Menu dan kawalan sidebar Streamlit dikekalkan secara asal. */

/* Ruang kandungan diselaraskan dengan header Streamlit asal. */
.block-container {
    padding: 1rem 2rem 2rem 2rem !important;
}
.card {
    background-color: #ffffff;
    border-left: 5px solid #2c3e50;
    padding: 1.3rem;
    border-radius: 10px;
    box-shadow: 3px 3px 12px rgba(0,0,0,0.08);
    text-align:center;
    min-height: 165px;
}
.metric-row {
    display: flex;
    justify-content: space-between;
    margin: 8px 0;
    font-size: 14px;
    gap: 14px;
}
.metric-label {color: #555; font-weight: 500;}
.metric-value {font-weight: bold;}
.traffic-circle {
    width: 95px;
    height: 95px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin: 8px auto 6px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}


/* =========================================================
   CLICKABLE TRAFFIC LIGHT - GAYA DASHBOARD PRESTASI
   Nombor dalam bulatan ialah button dan boleh ditekan.
   ========================================================= */
.traffic-range-jpka {
    width: 100%;
    text-align: center;
    font-size: 15px;
    font-weight: 900;
    color: #111827;
    margin: 2px 0 4px 0;
}

.traffic-caption-jpka {
    width: 100%;
    text-align: center;
    font-size: 17px;
    font-weight: 900;
    margin-top: 2px;
}

.st-key-btn_jpka_hijau button,
.st-key-btn_jpka_kuning button,
.st-key-btn_jpka_merah button {
    width: 138px !important;
    height: 138px !important;
    min-height: 138px !important;
    border-radius: 50% !important;
    margin: 10px auto 10px auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 44px !important;
    font-weight: 900 !important;
    position: relative !important;
    overflow: hidden !important;
    border: 4px solid rgba(255,255,255,0.38) !important;
    transition: all 0.18s ease-in-out !important;
    cursor: pointer !important;
    padding: 0 !important;
}

.st-key-btn_jpka_hijau,
.st-key-btn_jpka_kuning,
.st-key-btn_jpka_merah {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

.st-key-btn_jpka_hijau button {
    color: #ffffff !important;
    background: radial-gradient(circle at 30% 25%, #9dffad 0%, #2ee45a 42%, #07912b 100%) !important;
    box-shadow:
        0 0 18px rgba(46,228,90,0.60),
        0 0 38px rgba(46,228,90,0.36),
        0 16px 30px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.30),
        inset 0 -14px 20px rgba(0,0,0,0.28) !important;
    text-shadow: 0 3px 4px rgba(0,0,0,0.45), 0 0 12px rgba(255,255,255,0.28) !important;
}

.st-key-btn_jpka_kuning button {
    color: #263042 !important;
    background: radial-gradient(circle at 30% 25%, #fff9b5 0%, #f6d21e 43%, #b98a00 100%) !important;
    box-shadow:
        0 0 18px rgba(246,210,30,0.62),
        0 0 38px rgba(246,210,30,0.36),
        0 16px 30px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.42),
        inset 0 -14px 20px rgba(0,0,0,0.20) !important;
    text-shadow: 0 1px 0 rgba(255,255,255,0.70), 0 3px 4px rgba(0,0,0,0.28) !important;
}

.st-key-btn_jpka_merah button {
    color: #ffffff !important;
    background: radial-gradient(circle at 30% 25%, #ffaaaa 0%, #f04a42 42%, #a51218 100%) !important;
    box-shadow:
        0 0 18px rgba(240,74,66,0.62),
        0 0 38px rgba(240,74,66,0.36),
        0 16px 26px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.28),
        inset 0 -14px 20px rgba(0,0,0,0.30) !important;
    text-shadow: 0 3px 4px rgba(0,0,0,0.45), 0 0 12px rgba(255,255,255,0.25) !important;
}

.st-key-btn_jpka_hijau button:hover,
.st-key-btn_jpka_kuning button:hover,
.st-key-btn_jpka_merah button:hover {
    transform: translateY(-4px) scale(1.035) !important;
    border: 4px solid rgba(255,255,255,0.76) !important;
}

.st-key-btn_jpka_hijau button:active,
.st-key-btn_jpka_kuning button:active,
.st-key-btn_jpka_merah button:active {
    transform: translateY(4px) scale(0.98) !important;
}

.st-key-btn_jpka_hijau button p,
.st-key-btn_jpka_kuning button p,
.st-key-btn_jpka_merah button p {
    font-size: 44px !important;
    font-weight: 900 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e5e6 100%);
}

/* =========================================================
   SOFT CORPORATE GLASSMORPHISM THEME
   ========================================================= */

/* Main app background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 34%),
        radial-gradient(circle at top right, rgba(14,165,233,0.14), transparent 32%),
        linear-gradient(135deg, #eef4ff 0%, #f8fbff 45%, #e8f0fb 100%) !important;
}

/* Main page spacing */
.block-container {
    padding-top: 0.25rem !important;
    padding-bottom: 2rem !important;
}

/* Global headings */
h1, h2, h3 {
    letter-spacing: -0.3px;
}

/* Sidebar glass */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(15,23,42,0.92) 0%, rgba(30,58,138,0.88) 55%, rgba(15,23,42,0.92) 100%) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.16);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* Sidebar filter glass boxes */
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stRadio {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 18px !important;
    padding: 11px 11px 9px 11px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

/* Select input inside sidebar */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.96) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.38) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.30);
}

section[data-testid="stSidebar"] [data-baseweb="select"] span,
section[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #0f172a !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] button {
    border-radius: 999px !important;
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 18px rgba(0,0,0,0.14);
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.24) !important;
    border-color: rgba(255,255,255,0.55) !important;
}

/* Main KPI/card glass */
.card {
    background: rgba(255,255,255,0.72) !important;
    border: 1px solid rgba(255,255,255,0.68) !important;
    border-left: 5px solid rgba(37,99,235,0.76) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

/* Streamlit metric cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.68);
    border-radius: 20px;
    padding: 16px 18px;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

/* Expander as glass chart container */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.62) !important;
    border: 1px solid rgba(255,255,255,0.68) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 34px rgba(15,23,42,0.10);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    overflow: hidden;
}

div[data-testid="stExpander"] details summary {
    background: rgba(255,255,255,0.42) !important;
    border-radius: 18px !important;
    font-weight: 700 !important;
}

/* Tables/dataframes glass feel */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.70);
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
    overflow: hidden;
}

/* Plotly chart wrapper */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.56);
    border: 1px solid rgba(255,255,255,0.62);
    border-radius: 20px;
    padding: 8px;
    box-shadow: 0 14px 30px rgba(15,23,42,0.09);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

/* Traffic light circles softer glass */
.traffic-circle {
    box-shadow:
        0 12px 28px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.35) !important;
    border: 1px solid rgba(255,255,255,0.35);
}

/* Download / action buttons */
.stDownloadButton button,
.stButton button {
    border-radius: 999px !important;
    background: linear-gradient(90deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.42) !important;
    box-shadow: 0 10px 24px rgba(37,99,235,0.25);
    font-weight: 700 !important;
}

.stDownloadButton button:hover,
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(37,99,235,0.32);
}

/* Inputs in main area */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] {
    border-radius: 12px !important;
}

/* Hide default Streamlit details noise smoother */
hr {
    border-color: rgba(148,163,184,0.30) !important;
}


/* ===== SIDEBAR SCROLL BEHAVIOUR ===== */
/* Buang sticky/freeze behaviour sidebar navigation */
section[data-testid="stSidebar"] > div {
    position: relative !important;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    position: relative !important;
    top: auto !important;
}

/* Sidebar ikut scroll sekali */
section[data-testid="stSidebar"] {
    overflow-y: auto !important;
}



/* ===== FIX REFRESH BUTTON / SIDEBAR BUTTON SCROLL ===== */
/* Pastikan button dalam sidebar termasuk Refresh Data Excel tidak fixed/freeze */
section[data-testid="stSidebar"] .stButton,
section[data-testid="stSidebar"] .stButton button {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    z-index: auto !important;
}


/* Sidebar content scroll normal */
section[data-testid="stSidebar"] {
    overflow-y: auto !important;
}



</style>
""")



# =========================================================
# FINAL OVERRIDE: TRAFFIC LIGHT JPKA + CLICKABLE JUMLAH PTJ
# Diletakkan selepas CSS umum supaya warna tidak ditindih
# oleh style global .stButton button berwarna biru.
# =========================================================
st.markdown("""
<style>
/* Pastikan ketiga-tiga butang traffic light kekal bulat dan berwarna */
div[class*="st-key-btn_jpka_hijau"],
div[class*="st-key-btn_jpka_kuning"],
div[class*="st-key-btn_jpka_merah"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

div[class*="st-key-btn_jpka_hijau"] button,
div[class*="st-key-btn_jpka_kuning"] button,
div[class*="st-key-btn_jpka_merah"] button {
    width: 138px !important;
    height: 138px !important;
    min-height: 138px !important;
    max-width: 138px !important;
    border-radius: 50% !important;
    margin: 10px auto !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 4px solid rgba(255,255,255,0.42) !important;
    cursor: pointer !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}

div[class*="st-key-btn_jpka_hijau"] button {
    color: #ffffff !important;
    background: radial-gradient(circle at 30% 25%, #9dffad 0%, #2ee45a 42%, #07912b 100%) !important;
    box-shadow:
        0 0 18px rgba(46,228,90,0.62),
        0 0 38px rgba(46,228,90,0.38),
        0 16px 30px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.30),
        inset 0 -14px 20px rgba(0,0,0,0.28) !important;
    text-shadow: 0 3px 4px rgba(0,0,0,0.45), 0 0 12px rgba(255,255,255,0.28) !important;
}

div[class*="st-key-btn_jpka_kuning"] button {
    color: #263042 !important;
    background: radial-gradient(circle at 30% 25%, #fff9b5 0%, #f6d21e 43%, #b98a00 100%) !important;
    box-shadow:
        0 0 18px rgba(246,210,30,0.64),
        0 0 38px rgba(246,210,30,0.38),
        0 16px 30px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.42),
        inset 0 -14px 20px rgba(0,0,0,0.20) !important;
    text-shadow: 0 1px 0 rgba(255,255,255,0.72), 0 3px 4px rgba(0,0,0,0.28) !important;
}

div[class*="st-key-btn_jpka_merah"] button {
    color: #ffffff !important;
    background: radial-gradient(circle at 30% 25%, #ffaaaa 0%, #f04a42 42%, #a51218 100%) !important;
    box-shadow:
        0 0 18px rgba(240,74,66,0.64),
        0 0 38px rgba(240,74,66,0.38),
        0 16px 26px rgba(0,0,0,0.22),
        inset 0 9px 13px rgba(255,255,255,0.28),
        inset 0 -14px 20px rgba(0,0,0,0.30) !important;
    text-shadow: 0 3px 4px rgba(0,0,0,0.45), 0 0 12px rgba(255,255,255,0.25) !important;
}

div[class*="st-key-btn_jpka_hijau"] button:hover,
div[class*="st-key-btn_jpka_kuning"] button:hover,
div[class*="st-key-btn_jpka_merah"] button:hover {
    transform: translateY(-4px) scale(1.035) !important;
    border-color: rgba(255,255,255,0.82) !important;
}

div[class*="st-key-btn_jpka_hijau"] button p,
div[class*="st-key-btn_jpka_kuning"] button p,
div[class*="st-key-btn_jpka_merah"] button p {
    font-size: 44px !important;
    line-height: 1 !important;
    font-weight: 900 !important;
    margin: 0 !important;
    padding: 0 !important;
    color: inherit !important;
}

/* Jumlah PTJ sebagai nombor clickable tanpa rupa button biasa */
div[class*="st-key-btn_jumlah_ptj_jpka"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
}

div[class*="st-key-btn_jumlah_ptj_jpka"] > div,
div[class*="st-key-btn_jumlah_ptj_jpka"] [data-testid="stButton"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
}

div[class*="st-key-btn_jumlah_ptj_jpka"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #2c3e50 !important;
    min-height: 0 !important;
    height: auto !important;
    width: auto !important;
    padding: 0 !important;
    margin: 0 auto 2px auto !important;
    display: block !important;
    text-align: center !important;
}

div[class*="st-key-btn_jumlah_ptj_jpka"] button:hover {
    color: #2563eb !important;
    transform: scale(1.05) !important;
    text-decoration: underline !important;
    border: none !important;
}

div[class*="st-key-btn_jumlah_ptj_jpka"] button p {
    font-size: 46px !important;
    line-height: 1 !important;
    font-weight: 900 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.jpka-total-label {
    text-align: center;
    color: #2c3e50;
    font-size: 15px;
    font-weight: 900;
    margin-bottom: 10px;
}
.jpka-total-divider {
    border-top: 1px solid rgba(148,163,184,0.50);
    width: 88%;
    margin: 8px auto 10px auto;
}
.jpka-formula-line {
    text-align: center;
    margin: 4px 0;
    color: #2c3e50;
    font-size: 16px;
    line-height: 1.25;
}
.jpka-formula-highlight {
    text-align: center;
    color: #27ae60;
    margin: 14px 0 0 0;
    font-size: 19px;
    line-height: 1.25;
    font-weight: 900;
}
.jpka-total-wrap {
    width: 100%;
    padding-top: 11px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.jpka-total-wrap .jpka-total-label,
.jpka-total-wrap .jpka-formula-line,
.jpka-total-wrap .jpka-formula-highlight {
    width: 100%;
    text-align: center !important;
}

.jpka-total-wrap .jpka-total-divider {
    width: 88%;
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)



# =========================================================
# FULL SCREEN DASHBOARD - SIDEBAR KEKAL DIPAPARKAN
# Sama konsep seperti Dashboard Prestasi Program.
# - Full screen meliputi keseluruhan aplikasi Streamlit.
# - Sidebar tidak disembunyikan.
# - Tekan ESC untuk keluar daripada full screen.
# =========================================================
st.markdown("""
<style>
/* Gunakan keseluruhan ruang skrin tanpa mengecilkan sidebar. */
.main .block-container,
section.main .block-container,
div[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* Sidebar kekal pada saiz asal semasa full screen. */
section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
}

/* Butang full screen terapung di penjuru kanan atas. */
#jpka-fullscreen-toggle {
    position: fixed;
    top: 0.72rem;
    right: 4.3rem;
    z-index: 999999;
    width: 42px;
    height: 42px;
    border: 1px solid rgba(148,163,184,0.40);
    border-radius: 12px;
    background: rgba(255,255,255,0.88);
    color: #0f172a;
    box-shadow: 0 8px 24px rgba(15,23,42,0.16);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    cursor: pointer;
    font-size: 21px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.18s ease, box-shadow 0.18s ease,
                background 0.18s ease;
}

#jpka-fullscreen-toggle:hover {
    transform: translateY(-2px) scale(1.04);
    background: #ffffff;
    box-shadow: 0 12px 28px rgba(15,23,42,0.22);
}

#jpka-fullscreen-toggle:active {
    transform: translateY(1px) scale(0.98);
}

/* Dalam paparan telefon, rapatkan butang agar tidak bertindih. */
@media (max-width: 768px) {
    #jpka-fullscreen-toggle {
        top: 0.55rem;
        right: 3.65rem;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        font-size: 19px;
    }
}
</style>
""", unsafe_allow_html=True)

# Cipta butang dalam parent Streamlit supaya full screen merangkumi
# main dashboard dan sidebar sekali. Kod ini tidak mengubah function dashboard.
components.html(
    """
    <script>
    (function () {
        const doc = window.parent.document;
        const buttonId = "jpka-fullscreen-toggle";

        function isFullscreen() {
            return Boolean(
                doc.fullscreenElement ||
                doc.webkitFullscreenElement ||
                doc.msFullscreenElement
            );
        }

        function updateButton(button) {
            if (!button) return;
            const active = isFullscreen();
            button.innerHTML = active ? "⤢" : "⛶";
            button.title = active
                ? "Keluar paparan penuh (atau tekan ESC)"
                : "Paparan penuh";
            button.setAttribute(
                "aria-label",
                active ? "Keluar paparan penuh" : "Paparan penuh"
            );
        }

        function enterFullscreen() {
            const root = doc.documentElement;
            if (root.requestFullscreen) {
                return root.requestFullscreen();
            }
            if (root.webkitRequestFullscreen) {
                return root.webkitRequestFullscreen();
            }
            if (root.msRequestFullscreen) {
                return root.msRequestFullscreen();
            }
        }

        function exitFullscreen() {
            if (doc.exitFullscreen) {
                return doc.exitFullscreen();
            }
            if (doc.webkitExitFullscreen) {
                return doc.webkitExitFullscreen();
            }
            if (doc.msExitFullscreen) {
                return doc.msExitFullscreen();
            }
        }

        let button = doc.getElementById(buttonId);

        if (!button) {
            button = doc.createElement("button");
            button.id = buttonId;
            button.type = "button";
            doc.body.appendChild(button);

            button.addEventListener("click", function (event) {
                event.preventDefault();
                event.stopPropagation();

                try {
                    if (isFullscreen()) {
                        exitFullscreen();
                    } else {
                        enterFullscreen();
                    }
                } catch (error) {
                    console.error("Full screen tidak dapat dibuka:", error);
                }
            });
        }

        updateButton(button);

        if (!doc.__jpkaFullscreenListenerAdded) {
            doc.addEventListener("fullscreenchange", function () {
                updateButton(doc.getElementById(buttonId));
            });
            doc.addEventListener("webkitfullscreenchange", function () {
                updateButton(doc.getElementById(buttonId));
            });
            doc.__jpkaFullscreenListenerAdded = true;
        }
    })();
    </script>
    """,
    height=0,
    width=0
)

# =======================
# FUNGSI UMUM
# =======================
def format_nilai(nilai):
    """
    Format nombor kepada ringkasan RM.
    Contoh:
    130107903 -> RM 130.1 Juta
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0.0

    tanda = "-" if nilai < 0 else ""
    nilai_abs = abs(float(nilai))

    if nilai_abs >= 1_000_000_000:
        return f"{tanda}RM {nilai_abs / 1_000_000_000:.1f} Bilion"

    if nilai_abs >= 1_000_000:
        return f"{tanda}RM {nilai_abs / 1_000_000:.1f} Juta"

    if nilai_abs >= 1_000:
        return f"{tanda}RM {nilai_abs / 1_000:.1f} Ribu"

    return f"{tanda}RM {nilai_abs:.0f}"


def format_comma(nilai):
    """
    Format nombor dengan comma tanpa decimal.
    Contoh: 1234567 -> 1,234,567
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0

    return f"{nilai:,.0f}"


def format_comma_no_decimal(nilai):
    """
    Format nombor dengan comma tanpa decimal.
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        nilai = 0

    return f"{nilai:,.0f}"



def short_number(nilai):
    """
    Format nombor ringkas tanpa RM.
    Contoh:
    1,250,000   -> 1.3j
    980,000     -> 980.0k
    1,200,000,000 -> 1.2b
    """
    nilai = pd.to_numeric(nilai, errors="coerce")

    if pd.isna(nilai):
        return ""

    tanda = "-" if nilai < 0 else ""
    nilai_abs = abs(float(nilai))

    if nilai_abs >= 1_000_000_000:
        return f"{tanda}{nilai_abs / 1_000_000_000:.1f}b"

    if nilai_abs >= 1_000_000:
        return f"{tanda}{nilai_abs / 1_000_000:.1f}j"

    if nilai_abs >= 1_000:
        return f"{tanda}{nilai_abs / 1_000:.1f}k"

    return f"{tanda}{nilai_abs:,.0f}"

def dataframe_comma_style(df, money_cols=None, percent_cols=None):
    """
    Tukar column numeric tertentu kepada comma style untuk paparan report.
    """
    df_show = df.copy()

    if money_cols is None:
        money_cols = []

    if percent_cols is None:
        percent_cols = []

    for col in money_cols:
        if col in df_show.columns:
            df_show[col] = df_show[col].apply(format_comma)

    for col in percent_cols:
        if col in df_show.columns:
            df_show[col] = (
                pd.to_numeric(df_show[col], errors="coerce")
                .fillna(0)
                .map(lambda x: f"{x:,.2f}%")
            )

    return df_show


def hitung_prestasi(sebenar, sasaran):
    sebenar = pd.to_numeric(sebenar, errors="coerce")
    sasaran = pd.to_numeric(sasaran, errors="coerce")

    if pd.isna(sebenar):
        sebenar = 0.0
    if pd.isna(sasaran) or sasaran == 0:
        return 0.0

    return (sebenar / sasaran) * 100


def to_excel(df, sheet_name="Summary"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    output.seek(0)
    return output


def to_excel_multi(sheets):
    """
    Download beberapa dataframe dalam satu fail Excel.
    sheets = {"NamaSheet": dataframe}
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df_sheet in sheets.items():
            safe_sheet_name = str(sheet_name)[:31]
            df_sheet.to_excel(writer, index=False, sheet_name=safe_sheet_name)
    output.seek(0)
    return output


def bersih_nama_column(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df


def clean_numeric_series(series):
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").fillna(0)

    return (
        series.astype(str)
        .str.replace("RM", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


def pastikan_numeric(df, columns):
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = clean_numeric_series(df[col])
    return df


def unique_sorted(series):
    return sorted(series.dropna().astype(str).unique().tolist())


def natural_sort_key(value):
    """
    Susun teks secara natural:
    - Huruf ikut A-Z.
    - Nombor ikut 1, 2, 3, ... 10, 11, 12.
    - Elak susunan teks biasa seperti 1, 10, 11, 2.
    """
    import re

    value = "" if pd.isna(value) else str(value).strip()
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", value)
    ]



def kemas_label_bajet(trace):
    """Tukar nama legend chart kepada label ringkas."""
    trace.name = (
        str(trace.name)
        .replace("BAJET_JT", "Bajet")
        .replace("SASARAN_JT", "Bajet Qtr")
        .replace("SEBENAR_JT", "Sebenar")
        .replace("BAJET 2025", "Bajet")
        .replace("SASARAN Q1-25", "Bajet Qtr")
        .replace("SEBENAR Q1-25", "Sebenar")
    )
    return trace


def rename_summary_columns(df):
    """Tukar nama column output kepada label ringkas."""
    return df.rename(columns={
        "PTJ1": "PTJ",
        "DESC": "Item",
        "Quarter": "Tempoh",
        "KOD1": "Kod Item",
        "BAJET 2025": "Bajet",
        "SASARAN Q1-25": "Bajet Qtr",
        "SEBENAR Q1-25": "Sebenar 06-2026",
        "SEBENAR 06-2025": "Sebenar 06-2025"
    })



def apply_geran_arrow_labels(fig, orientation="v", threshold_ratio=0.18):
    """
    Label Geran:
    - Text mendatar.
    - Nilai kecil/bertindih dialihkan kepada annotation dengan arrow.
    - Text asal untuk nilai tersebut disembunyikan supaya tidak overlap.
    """
    try:
        for trace in fig.data:
            if getattr(trace, "type", "") != "bar":
                continue

            is_horizontal = orientation == "h" or getattr(trace, "orientation", None) == "h"

            vals = list(trace.x) if is_horizontal else list(trace.y)
            cats = list(trace.y) if is_horizontal else list(trace.x)

            if not vals:
                continue

            numeric_vals = [
                abs(float(pd.to_numeric(v, errors="coerce")))
                for v in vals
                if not pd.isna(pd.to_numeric(v, errors="coerce"))
            ]

            if not numeric_vals:
                continue

            max_val = max(numeric_vals)
            if max_val <= 0:
                continue

            text_list = list(trace.text) if trace.text is not None else [
                format_nilai(v) for v in vals
            ]

            new_text = list(text_list)

            for i, val in enumerate(vals):
                val_num = pd.to_numeric(val, errors="coerce")

                if pd.isna(val_num) or float(val_num) == 0:
                    continue

                # Nilai kecil berpotensi bertindih, jadi guna arrow.
                if abs(float(val_num)) <= max_val * threshold_ratio:
                    label = str(text_list[i]) if i < len(text_list) else format_nilai(val_num)

                    if is_horizontal:
                        fig.add_annotation(
                            x=float(val_num),
                            y=cats[i],
                            text=label,
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=0.8,
                            arrowwidth=1,
                            arrowcolor="rgba(80,80,80,0.70)",
                            ax=55 + ((i % 3) * 18),
                            ay=0,
                            font=dict(
                                size=11,
                                color="black",
                                family="Arial"
                            ),
                            bgcolor="rgba(255,255,255,0.88)",
                            bordercolor="rgba(120,120,120,0.35)",
                            borderwidth=0.5,
                            borderpad=2
                        )
                    else:
                        fig.add_annotation(
                            x=cats[i],
                            y=float(val_num),
                            text=label,
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=0.8,
                            arrowwidth=1,
                            arrowcolor="rgba(80,80,80,0.70)",
                            ax=0,
                            ay=-35 - ((i % 4) * 14),
                            font=dict(
                                size=11,
                                color="black",
                                family="Arial"
                            ),
                            bgcolor="rgba(255,255,255,0.88)",
                            bordercolor="rgba(120,120,120,0.35)",
                            borderwidth=0.5,
                            borderpad=2
                        )

                    if i < len(new_text):
                        new_text[i] = ""

            trace.text = new_text
            trace.texttemplate = "%{text}"
            trace.textposition = "outside"
            trace.textangle = 0
            trace.cliponaxis = False
            trace.constraintext = "none"
            trace.textfont = dict(
                size=11,
                color="black",
                family="Arial"
            )

        fig.update_layout(
            margin=dict(t=170, b=160, l=90, r=110),
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        fig.update_xaxes(automargin=True)
        fig.update_yaxes(automargin=True)

    except Exception:
        pass

    return fig



def apply_chart_text_style(fig, size=12, angle=0):
    """
    Paksa nilai/amount keluar pada semua bar chart.
    Tidak apply kepada scatter/line.
    """
    for trace in fig.data:
        if getattr(trace, "type", "") == "bar":
            orientasi = getattr(trace, "orientation", None)

            values = list(trace.x) if orientasi == "h" else list(trace.y)
            current_text = list(trace.text) if trace.text is not None else []

            if not current_text or all(str(x).strip().lower() in ["", "none", "nan", "null"] for x in current_text):
                fallback_text = []

                for val in values:
                    val_num = pd.to_numeric(val, errors="coerce")

                    if pd.isna(val_num):
                        fallback_text.append("")
                    elif abs(float(val_num)) >= 1_000:
                        fallback_text.append(format_nilai(val_num))
                    else:
                        fallback_text.append(f"{float(val_num):,.2f}")

                trace.text = fallback_text

            trace.texttemplate = "%{text}"
            trace.textposition = "outside"
            trace.textangle = angle
            trace.cliponaxis = False
            trace.constraintext = "none"
            trace.textfont = dict(
                size=size,
                family="Arial",
                color="black"
            )

    fig.update_layout(
        margin=dict(t=180, b=150, l=90, r=100),
        uniformtext_minsize=6,
        uniformtext_mode="show"
    )

    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig


def detect_amount_column(df):
    calon = [
        "Amount in local currency", "AMOUNT IN LOCAL CURRENCY",
        "JUMLAH", "Jumlah", "AMAUN", "Amaun", "AMOUNT", "Amount",
        "NILAI", "Nilai", "BAKI", "Baki", "BALANCE", "Balance",
        "DEBIT", "Debit", "KREDIT", "Kredit", "CREDIT", "Credit",
        "RM", "TOTAL", "Total"
    ]

    for col in calon:
        if col in df.columns:
            return col

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        return numeric_cols[0]

    for col in df.columns:
        converted = clean_numeric_series(df[col])
        if converted.abs().sum() > 0:
            return col

    return None


# =======================
# LOAD DATA BELANJA & HASIL
# Nota:
# - Belanja & Hasil kini guna SATU fail Excel sahaja:
#   JPKA_ANALISA PK CIDB 06-2026.xlsx
# - Comparison Carta 2 menggunakan column dalam fail yang sama:
#   SEBENAR 06-2025
# =======================
@st.cache_data(show_spinner="Memuatkan data Belanja & Hasil...")
def load_data():
    df_dict = {}
    errors = []

    files = {
        "06-2026": "JPKA_ANALISA PK CIDB 06-2026.xlsx"
    }

    for q, filename in files.items():
        try:
            df = pd.read_excel(
                filename,
                sheet_name="All2",
                engine="openpyxl"
            )
            df = bersih_nama_column(df)

            if "KOD" in df.columns and "KOD1" not in df.columns:
                df = df.rename(columns={"KOD": "KOD1"})

            rename_map = {
                # Header baharu Q2 -> nama dalaman lama supaya semua function asal kekal
                "BAJET 2026": "BAJET 2025",
                "Bajet 2026": "BAJET 2025",
                "BAJET2026": "BAJET 2025",
                "BAJET 06-2026": "SASARAN Q1-25",
                "SASARAN Q2-26": "SASARAN Q1-25",
                "SASARAN 06-2026": "SASARAN Q1-25",
                "BAJET QTR": "SASARAN Q1-25",
                "SEBENAR Q2-26": "SEBENAR Q1-25",
                "SEBENAR 06-2026": "SEBENAR Q1-25",
                "SEBENAR 06-2025": "SEBENAR 06-2025",
                # Header legacy dalam fail massage turut disokong
                "SASARAN Q1-25": "SASARAN Q1-25",
                "SEBENAR Q1-25": "SEBENAR Q1-25",
                "PRESTASI 03-2025": "PRESTASI 03-2025"
            }

            safe_rename = {}
            for old_col, new_col in rename_map.items():
                if old_col in df.columns:
                    if old_col == new_col or new_col not in df.columns:
                        safe_rename[old_col] = new_col

            df = df.rename(columns=safe_rename)

            if "SEBENAR 06-2025" not in df.columns:
                # Jika fail hanya ada nisbah PRESTASI 03-2025 bagi item mengurus,
                # anggarkan nilai tahun lepas = sebenar semasa / nisbah.
                if "PRESTASI 03-2025" in df.columns:
                    ratio = pd.to_numeric(df["PRESTASI 03-2025"], errors="coerce")
                    current = pd.to_numeric(df.get("SEBENAR Q1-25", 0), errors="coerce").fillna(0)
                    df["SEBENAR 06-2025"] = current.where(ratio.isna() | (ratio == 0), current / ratio)
                else:
                    df["SEBENAR 06-2025"] = 0

            df["Sumber"] = q
            df["Quarter"] = q
            df["Tahun"] = int(q.split("-")[1])

            numeric_cols = [
                "BAJET 2025",
                "SASARAN Q1-25",
                "SEBENAR Q1-25",
                "SEBENAR 06-2025"
            ]
            df = pastikan_numeric(df, numeric_cols)

            text_columns = [
                "PTJ", "PTJ1", "Kategori", "DESC", "KOD1",
                "Sumber", "Quarter"
            ]
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].fillna("").astype(str).str.strip()

            df_dict[q] = df

        except Exception as e:
            errors.append(f"{q} - {filename}: {e}")

    return df_dict, errors


# =======================
# LOAD DATA GERAN - WORKSHEET DATA SAHAJA
# Nota: tidak guna cache supaya perubahan Excel terus dibaca semula.
# =======================
@st.cache_data(show_spinner="Memuatkan data Geran...")
def load_data_geran():
    filename = "3-GL ADV 06-2026 24072026.XLSX"

    try:
        df_data = pd.read_excel(
            filename,
            sheet_name="DATA",
            engine="openpyxl"
        )
        df_data = bersih_nama_column(df_data)

        # Fail Q2 tidak semestinya mempunyai NAMA1. Bina label ringkas tanpa ubah NAMA asal.
        if "NAMA1" not in df_data.columns and "NAMA" in df_data.columns:
            nama_ringkas = {
                "CIDB Holdings Sdn Bhd": "CIDB HOLDINGS",
                "CIDB Digital Sdn Bhd": "CIDB DIGITAL",
                "CREAM": "CREAM",
                "CLAB": "CLAB",
                "ABM Selangor Sdn Bhd": "ABM SELANGOR",
                "ABM Johor Sdn Bhd": "ABM JOHOR",
                "ABM Utara Sdn Bhd": "ABM UTARA",
                "ABM Terengganu Sdn Bhd": "ABM TERENGGANU",
                "ABM Sabah Sdn Bhd": "ABM SABAH",
                "ABM Sarawak Sdn Bhd": "ABM SARAWAK",
                "CIDB IBS Sdn Bhd": "CIDB IBS",
                "CIDB Technologies Sdn Bhd": "CIDB TECHNOLOGIES",
            }
            clean_nama = df_data["NAMA"].fillna("").astype(str).str.strip()
            df_data["NAMA1"] = clean_nama.map(nama_ringkas).fillna(clean_nama)

        for col in ["NAMA", "NAMA1", "LEGEND", "PTJ"]:
            if col in df_data.columns:
                df_data[col] = (
                    df_data[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        return df_data, ""

    except Exception as e:
        return pd.DataFrame(), f"{filename}: {e}"


# =======================
# PREPARE DATA
# =======================
df_dict, belanja_errors = load_data()
df_geran, geran_error = load_data_geran()

# =======================
# MENU UTAMA DI MAIN PAGE
# Tajuk besar dibuang kerana setiap modul sudah mempunyai subtajuk sendiri.
# =======================

menu_label = st.pills(
    "Pilih Modul",
    options=["Belanja & Hasil", "Geran", "P&L", "Balance Sheet", "Cash Flow"],
    default="Belanja & Hasil",
    label_visibility="collapsed"
)

menu_map = {
    "Belanja & Hasil": "1. Belanja & Hasil",
    "Geran": "2. Geran",
    "P&L": "3. P&L",
    "Balance Sheet": "4. Balance Sheet",
    "Cash Flow": "5. Cash Flow",
}

menu = menu_map.get(menu_label, "1. Belanja & Hasil")

tajuk_utama = {
    "1. Belanja & Hasil": "📊 PRESTASI PERBELANJAAN DAN HASIL CIDB SEHINGGA SUKU KEDUA 2026",
    "2. Geran": "📊 PRESTASI GERAN SEHINGGA SUKU KEDUA 2026",
    "3. P&L": "📊 Profit & Loss",
    "4. Balance Sheet": "📊 Balance Sheet",
    "5. Cash Flow": "📊 Cash Flow",
}

html(f"""
<h2 style="text-align:center; font-weight:700; font-size:22px; color:#334155; margin-top:8px; margin-bottom:16px;">
    {tajuk_utama.get(menu, "📊 PRESTASI KEWANGAN CIDB")}
</h2>
""")

st.sidebar.markdown("### 🔎 Slicer / Filter")
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["dashboard_authenticated"] = False
    st.rerun()
if st.sidebar.button(
    "🔄 Refresh Data Excel",
    use_container_width=True,
    key="refresh_semua_data_excel"
):
    st.cache_data.clear()

    for state_key in [
        "_geran_slicer_base_df_stable",
        "_geran_slicer_base_df_full"
    ]:
        if state_key in st.session_state:
            del st.session_state[state_key]

    st.toast("Data Excel sedang dimuatkan semula.", icon="🔄")
    st.rerun()



# =======================
# MENU 1: BELANJA & HASIL
# =======================
if menu == "1. Belanja & Hasil":
    if not df_dict:
        st.error("Data Belanja & Hasil tidak berjaya dimuatkan.")
        if belanja_errors:
            with st.expander("Lihat detail error file", expanded=True):
                for err in belanja_errors:
                    st.write(f"- {err}")
        st.stop()

    quarters_available = [q for q in ["06-2026"] if q in df_dict]

    with st.sidebar:
        st.markdown("### 🔎 PILIHAN ")

    # Tempoh global tidak dipaparkan sebagai slicer.
    # Dashboard utama auto guna tempoh terkini.
    # Carta 2 masih ada filter comparison tempoh sendiri.
    pilih_quarter = ["06-2026"] if "06-2026" in quarters_available else quarters_available[-1:]

    if not pilih_quarter:
        st.warning("Tiada tempoh data tersedia.")
        st.stop()

    dfs = [df_dict[q] for q in pilih_quarter if q in df_dict]
    if not dfs:
        st.warning("Tiada data untuk Quarter yang dipilih.")
        st.stop()

    df_tapis = pd.concat(dfs, ignore_index=True)
    df_tapis = bersih_nama_column(df_tapis)

    required_cols = [
        "PTJ", "PTJ1", "Kategori", "DESC", "KOD1",
        "BAJET 2025", "SASARAN Q1-25", "SEBENAR Q1-25", "SEBENAR 06-2025", "Quarter"
    ]
    missing_cols = [col for col in required_cols if col not in df_tapis.columns]
    if missing_cols:
        st.error("Column berikut tiada dalam data Belanja & Hasil:")
        st.write(missing_cols)
        st.stop()

    # =======================
    # PILLS + TICK SLICER ENGINE
    # BELANJA & HASIL
    #
    # Konsep:
    # - Semua slicer guna pills.
    # - Pilihan yang selected dipaparkan dengan ✅.
    # - Pilihan yang belum selected dipaparkan dengan ◻️.
    # - Klik pill = toggle pilih/buang.
    # - Empty selected = ALL.
    # - Options setiap slicer dikira berdasarkan filter lain.
    # =======================

    def _as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def _unique_col(df_source, col):
        if col not in df_source.columns:
            return []
        return unique_sorted(df_source[col])

    def _filter_df(df_source, filters, exclude_col=None):
        df_temp = df_source.copy()

        for col, vals in filters.items():
            if exclude_col is not None and col == exclude_col:
                continue

            vals = _as_list(vals)
            if vals and col in df_temp.columns:
                df_temp = df_temp[
                    df_temp[col].astype(str).isin(vals)
                ]

        return df_temp

    def _get_belanja_filter_state():
        return {
            "Kategori": _as_list(st.session_state.get("belanja_kategori_final2", [])),
            "PTJ": _as_list(st.session_state.get("belanja_pejabat_final2", [])),
            "PTJ1": _as_list(st.session_state.get("belanja_ptj_final2", [])),
            "DESC": _as_list(st.session_state.get("belanja_item_final2", [])),
            "KOD1": _as_list(st.session_state.get("belanja_kod_item_final2", [])),
        }

    def _set_belanja_filter_value(col, values):
        values = _as_list(values)

        if col == "Kategori":
            st.session_state["belanja_kategori_final2"] = values
        elif col == "PTJ":
            st.session_state["belanja_pejabat_final2"] = values
        elif col == "PTJ1":
            st.session_state["belanja_ptj_final2"] = values
        elif col == "DESC":
            st.session_state["belanja_item_final2"] = values
        elif col == "KOD1":
            st.session_state["belanja_kod_item_final2"] = values

    def _clean_filter_values(df_source):
        """
        Buang selected value yang sudah tidak wujud.
        Empty tetap bermaksud ALL.
        """
        filters = _get_belanja_filter_state()

        for col, vals in filters.items():
            valid = set(_unique_col(df_source, col))
            cleaned = [
                x for x in _as_list(vals)
                if x in valid
            ]
            _set_belanja_filter_value(col, cleaned)

    def _options_for_slicer(df_source, col):
        """
        Options untuk slicer dikira berdasarkan semua filter lain,
        kecuali filter dirinya sendiri.
        """
        filters = _get_belanja_filter_state()
        df_context = _filter_df(
            df_source,
            filters,
            exclude_col=col
        )
        return _unique_col(df_context, col)

    def _pill_label(value, selected_values):
        selected_set = set(_as_list(selected_values))
        return f"✅ {value}" if value in selected_set else f"◻️ {value}"

    def _remove_tick_icon(label):
        label = str(label)
        label = label.replace("✅ ", "", 1)
        label = label.replace("◻️ ", "", 1)
        return label.strip()

    def _sync_pill_toggle(col, pill_key, selected_key):
        """
        Toggle behaviour:
        - Jika pill belum selected, klik akan add.
        - Jika pill sudah selected, klik akan remove.
        """
        raw_clicked = _as_list(st.session_state.get(pill_key, []))
        if not raw_clicked:
            return

        clicked_values = [
            _remove_tick_icon(x)
            for x in raw_clicked
        ]

        current_selected = _as_list(st.session_state.get(selected_key, []))
        selected_set = set(current_selected)

        for value in clicked_values:
            if value in selected_set:
                selected_set.remove(value)
            else:
                selected_set.add(value)

        new_selected = sorted(list(selected_set))
        st.session_state[selected_key] = new_selected

        # Kekalkan expander filter ini terbuka selepas pill diklik.
        # Tanpa ini, Streamlit rerun akan tutup balik filter.
        st.session_state[f"{selected_key}_expanded"] = True

        # Clear temporary clicked pills supaya boleh klik semula.
        st.session_state[pill_key] = []

    def _render_pill_slicer(title, col, selected_key, pill_key, df_source):
        """
        Render slicer dalam bentuk expander.
        Tajuk sahaja dipaparkan dahulu.
        Bila klik tajuk, pills akan muncul.
        """
        options = _options_for_slicer(
            df_source,
            col
        )

        current_selected = [
            x for x in _as_list(st.session_state.get(selected_key, []))
            if x in set(options)
        ]
        st.session_state[selected_key] = current_selected

        if current_selected:
            expander_title = f"{title}  ✅ {len(current_selected)}/{len(options)}"
        else:
            expander_title = f"{title}  🌐 All ({len(options)})"

        expanded_key = f"{selected_key}_expanded"

        with st.expander(
            expander_title,
            expanded=st.session_state.get(expanded_key, False)
        ):
            if current_selected:
                st.caption(f"Selected: {len(current_selected)} / {len(options)}")
            else:
                st.caption(f"All selected secara automatik: {len(options)} item")

            pill_options = [
                _pill_label(x, current_selected)
                for x in options
            ]

            st.pills(
                title,
                options=pill_options,
                selection_mode="multi",
                key=pill_key,
                label_visibility="collapsed",
                on_change=lambda: _sync_pill_toggle(
                    col,
                    pill_key,
                    selected_key
                )
            )

    with st.sidebar:

        df_slicer_base = df_tapis.copy()

        # Buang state lama yang tidak digunakan.
        legacy_keys = [
            "belanja_lock_kategori",
            "belanja_lock_pejabat",
            "belanja_lock_ptj",
            "belanja_lock_item",
            "belanja_lock_kod_item",
        ]

        for legacy_key in legacy_keys:
            if legacy_key in st.session_state:
                del st.session_state[legacy_key]

        # Initialize selected keys.
        selected_keys = [
            "belanja_kategori_final2",
            "belanja_pejabat_final2",
            "belanja_ptj_final2",
            "belanja_item_final2",
            "belanja_kod_item_final2",
        ]

        for key in selected_keys:
            if key not in st.session_state:
                st.session_state[key] = []

        _clean_filter_values(df_slicer_base)

        _render_pill_slicer(
            "📂 Pilih Kategori",
            "Kategori",
            "belanja_kategori_final2",
            "belanja_kategori_pills_tick",
            df_slicer_base
        )

        _render_pill_slicer(
            "🏢 Pilih Pejabat",
            "PTJ",
            "belanja_pejabat_final2",
            "belanja_pejabat_pills_tick",
            df_slicer_base
        )

        _render_pill_slicer(
            "⚡ Pilih PTJ",
            "PTJ1",
            "belanja_ptj_final2",
            "belanja_ptj_pills_tick",
            df_slicer_base
        )

        _render_pill_slicer(
            "🧾 Pilih Item",
            "DESC",
            "belanja_item_final2",
            "belanja_item_pills_tick",
            df_slicer_base
        )

        _render_pill_slicer(
            "🔢 Pilih Kod Item",
            "KOD1",
            "belanja_kod_item_final2",
            "belanja_kod_item_pills_tick",
            df_slicer_base
        )

        active_count = sum(
            1 for vals in _get_belanja_filter_state().values()
            if _as_list(vals)
        )
        st.caption(f"Filter aktif: {active_count}/5")

        if st.button("♻️ Reset Slicer Belanja & Hasil", key="reset_slicer_belanja_final2"):
            for key in [
                "belanja_pejabat_final2",
                "belanja_ptj_final2",
                "belanja_kategori_final2",
                "belanja_item_final2",
                "belanja_kod_item_final2",
                "belanja_kategori_pills_tick",
                "belanja_pejabat_pills_tick",
                "belanja_ptj_pills_tick",
                "belanja_item_pills_tick",
                "belanja_kod_item_pills_tick",
                "belanja_kategori_final2_expanded",
                "belanja_pejabat_final2_expanded",
                "belanja_ptj_final2_expanded",
                "belanja_item_final2_expanded",
                "belanja_kod_item_final2_expanded",
                "belanja_final2_slicer_initialized",
                "ptj_pills_multi_final2",
                "item_pills_multi_final2",
                "kod_pills_multi_final2",
                "belanja_lock_kategori",
                "belanja_lock_pejabat",
                "belanja_lock_ptj",
                "belanja_lock_item",
                "belanja_lock_kod_item",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    pilih_ptj = _as_list(st.session_state.get("belanja_pejabat_final2", []))
    pilih_ptj1 = _as_list(st.session_state.get("belanja_ptj_final2", []))
    pilih_kategori = _as_list(st.session_state.get("belanja_kategori_final2", []))
    pilih_desc = _as_list(st.session_state.get("belanja_item_final2", []))
    pilih_kod1 = _as_list(st.session_state.get("belanja_kod_item_final2", []))

    active_filters_final = {
        "Kategori": pilih_kategori,
        "PTJ": pilih_ptj,
        "PTJ1": pilih_ptj1,
        "DESC": pilih_desc,
        "KOD1": pilih_kod1,
    }

    # Empty selection = ALL.
    df_tapis = _filter_df(
        df_tapis,
        active_filters_final
    )

    if df_tapis.empty:
        st.warning("Tiada data selepas tapisan dibuat.")
        st.stop()

    df_akhir = df_tapis.copy()
    df_akhir["Jenis_Belanja"] = df_akhir["Kategori"].apply(
        lambda x:
        "Mengurus" if "Mengurus" in str(x) else
        "Program" if "Program" in str(x) else
        "Modal" if "Modal" in str(x) else
        "Hasil" if "Hasil" in str(x) else
        "Lain-lain"
    )

    st.markdown("### 🚦 STATUS PRESTASI PTJ")

    df_akhir["Prestasi_%"] = df_akhir.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    df_group = df_akhir.groupby("PTJ1", as_index=False).agg({
        "BAJET 2025": "sum",
        "SASARAN Q1-25": "sum",
        "SEBENAR Q1-25": "sum"
    })

    # Prestasi_% lama dikekalkan untuk status lampu / drilldown.
    # Formula lama: Sebenar / Sasaran
    df_group["Prestasi_%"] = df_group.apply(
        lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    # Formula baharu untuk Carta 4:
    # % Prestasi   = SEBENAR / BAJET
    # % Sasaran    = SASARAN / BAJET
    # % Pencapaian = SEBENAR / SASARAN

    # Jika BAJET kosong / 0:
    # - Papar nilai graf = 0%
    # - Papar nota #DIV/0! pada label

    df_group["Nota_DIV0"] = df_group["BAJET 2025"].apply(
        lambda x: "#DIV/0!" if pd.to_numeric(x, errors="coerce") in [0, 0.0] else ""
    )

    df_group["% Prestasi"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["BAJET 2025"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SEBENAR Q1-25"], row["BAJET 2025"]),
        axis=1
    )

    df_group["% Sasaran"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["BAJET 2025"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SASARAN Q1-25"], row["BAJET 2025"]),
        axis=1
    )

    df_group["% Pencapaian"] = df_group.apply(
        lambda row: 0
        if pd.to_numeric(row["SASARAN Q1-25"], errors="coerce") in [0, 0.0]
        else hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
        axis=1
    )

    hebat = len(df_group[df_group["Prestasi_%"] > 95])
    bagus = len(df_group[(df_group["Prestasi_%"] >= 85) & (df_group["Prestasi_%"] <= 94.99)])
    usaha = len(df_group[df_group["Prestasi_%"] < 85])
    total = len(df_group)

    total_bajet = df_akhir["BAJET 2025"].sum()
    total_sebenar = df_akhir["SEBENAR Q1-25"].sum()
    total_sasaran = df_akhir["SASARAN Q1-25"].sum()

    # Area traffic light:
    # SASARAN    = Sasaran / Bajet
    # PRESTASI   = Sebenar / Bajet
    # PENCAPAIAN = Sebenar / Sasaran
    sasaran_pct = hitung_prestasi(total_sasaran, total_bajet)
    prestasi_pct = hitung_prestasi(total_sebenar, total_bajet)
    pencapaian = hitung_prestasi(total_sebenar, total_sasaran)

    sasaran_int = round(sasaran_pct)
    prestasi_int = round(prestasi_pct)
    pencapaian_int = round(pencapaian)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

    if "show_drill_belanja" not in st.session_state:
        st.session_state.show_drill_belanja = None
        st.session_state.drill_title_belanja = ""

    with col1:
        html("""
        <div class="traffic-range-jpka">&gt; 95%</div>
        """)
        if st.button(f"{hebat}", key="btn_jpka_hijau"):
            st.session_state.show_drill_belanja = "hebat"
            st.session_state.drill_title_belanja = "Senarai PTJ Hebat (> 95%)"
            st.rerun()
        html("""
        <div class="traffic-caption-jpka" style="color:#07912b;">Hebat!</div>
        """)

    with col2:
        html("""
        <div class="traffic-range-jpka">85% - 94.99%</div>
        """)
        if st.button(f"{bagus}", key="btn_jpka_kuning"):
            st.session_state.show_drill_belanja = "bagus"
            st.session_state.drill_title_belanja = "Senarai PTJ Bagus (85% - 94.99%)"
            st.rerun()
        html("""
        <div class="traffic-caption-jpka" style="color:#b98a00;">Bagus!</div>
        """)

    with col3:
        html("""
        <div class="traffic-range-jpka">&lt; 85%</div>
        """)
        if st.button(f"{usaha}", key="btn_jpka_merah"):
            st.session_state.show_drill_belanja = "usaha"
            st.session_state.drill_title_belanja = "Senarai PTJ Usaha Lagi (< 85%)"
            st.rerun()
        html("""
        <div class="traffic-caption-jpka" style="color:#a51218;">Usaha lagi!</div>
        """)

    with col4:
        html('<div class="jpka-total-wrap">')
        if st.button(f"{total}", key="btn_jumlah_ptj_jpka"):
            st.session_state.show_drill_belanja = "semua"
            st.session_state.drill_title_belanja = "Senarai Keseluruhan PTJ"
            st.rerun()

        html(f"""
        <div class="jpka-total-label">Jumlah PTJ</div>
        <div class="jpka-total-divider"></div>
        <p class="jpka-formula-line" title="Formula: Bajet Qtr / Bajet Tahunan">
            <strong>SASARAN</strong> {sasaran_int}%
        </p>
        <p class="jpka-formula-line" title="Formula: Sebenar / Bajet Tahunan">
            <strong>PRESTASI</strong> {prestasi_int}%
        </p>
        <p class="jpka-formula-highlight" title="Formula: Prestasi / Sasaran">
            PENCAPAIAN {pencapaian_int}%
        </p>
        </div>
        """)

    if st.session_state.show_drill_belanja:
        st.subheader(st.session_state.drill_title_belanja)
        if st.session_state.show_drill_belanja == "hebat":
            df_show = df_group[df_group["Prestasi_%"] > 95].sort_values("Prestasi_%", ascending=False)
        elif st.session_state.show_drill_belanja == "bagus":
            df_show = df_group[
                (df_group["Prestasi_%"] >= 85) &
                (df_group["Prestasi_%"] <= 94.99)
            ].sort_values("Prestasi_%", ascending=False)
        elif st.session_state.show_drill_belanja == "usaha":
            df_show = df_group[df_group["Prestasi_%"] < 85].sort_values("Prestasi_%", ascending=False)
        else:
            # Klik Jumlah PTJ: papar semua PTJ tanpa tapisan traffic light.
            df_show = df_group.copy()

        # Default senarai: Pencapaian (%) tertinggi ke terendah.
        # Nilai kewangan dan peratus KEKAL sebagai nombor supaya apabila
        # pengguna klik tajuk column, Streamlit menyusun secara numeric:
        # 1, 2, 3, ... 10, 11 (bukan 1, 10, 11, 2).
        if not df_show.empty:
            df_show = (
                df_show
                .sort_values(
                    by=["Prestasi_%", "PTJ1"],
                    ascending=[False, True],
                    kind="mergesort"
                )
                .reset_index(drop=True)
            )

        if not df_show.empty:
            df_show_list = df_show[[
                "PTJ1",
                "BAJET 2025",
                "SASARAN Q1-25",
                "SEBENAR Q1-25",
                "Prestasi_%"
            ]].copy()

            df_show_list = df_show_list.rename(columns={
                "PTJ1": "PTJ",
                "BAJET 2025": "Bajet Tahunan",
                "SASARAN Q1-25": "Bajet Qtr",
                "SEBENAR Q1-25": "Sebenar",
                "Prestasi_%": "Pencapaian (%)"
            })

            # Pastikan column angka benar-benar numeric untuk sorting header.
            for numeric_col in [
                "Bajet Tahunan",
                "Bajet Qtr",
                "Sebenar",
                "Pencapaian (%)"
            ]:
                df_show_list[numeric_col] = pd.to_numeric(
                    df_show_list[numeric_col],
                    errors="coerce"
                ).fillna(0)

            # PTJ menggunakan susunan kategori natural A-Z / nombor sebenar.
            # Ini membantu sorting PTJ seperti PTJ 1, PTJ 2, ... PTJ 10.
            ptj_categories = sorted(
                df_show_list["PTJ"].astype(str).unique().tolist(),
                key=natural_sort_key
            )
            df_show_list["PTJ"] = pd.Categorical(
                df_show_list["PTJ"].astype(str),
                categories=ptj_categories,
                ordered=True
            )

            st.caption(
                "Default: Pencapaian (%) tertinggi. Klik tajuk column untuk susun menaik/menurun."
            )

            st.dataframe(
                df_show_list,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "PTJ": st.column_config.TextColumn("PTJ"),
                    "Bajet Tahunan": st.column_config.NumberColumn(
                        "Bajet Tahunan",
                        format="%,.0f"
                    ),
                    "Bajet Qtr": st.column_config.NumberColumn(
                        "Bajet Qtr",
                        format="%,.0f"
                    ),
                    "Sebenar": st.column_config.NumberColumn(
                        "Sebenar",
                        format="%,.0f"
                    ),
                    "Pencapaian (%)": st.column_config.NumberColumn(
                        "Pencapaian (%)",
                        format="%.2f%%"
                    )
                }
            )
        else:
            st.info("Tiada rekod untuk kategori ini.")

        if st.button("❌ Tutup Senarai", type="primary"):
            st.session_state.show_drill_belanja = None
            st.rerun()

    with st.expander("📋 RINGKASAN KESELURUHAN", expanded=False):
        for q in pilih_quarter:
            df_q = df_akhir[df_akhir["Quarter"] == q]
            with st.expander(f"Tempoh {q}", expanded=True):
                col_k1, col_k2, col_k3, col_k4 = st.columns(4)
                jenis_list = [
                    ("Mengurus", "BELANJA MENGURUS", col_k1),
                    ("Program", "BELANJA PROGRAM", col_k2),
                    ("Modal", "BELANJA MODAL", col_k3),
                    ("Hasil", "HASIL", col_k4)
                ]
                for jenis, tajuk, col in jenis_list:
                    b = df_q[df_q["Jenis_Belanja"] == jenis]["BAJET 2025"].sum()
                    s = df_q[df_q["Jenis_Belanja"] == jenis]["SASARAN Q1-25"].sum()
                    se = df_q[df_q["Jenis_Belanja"] == jenis]["SEBENAR Q1-25"].sum()
                    with col:
                        html(f"""
                        <div class="card">
                            <h4 style="text-align:center; color:#2c3e50;">{tajuk}</h4>
                            <div class="metric-row">
                                <span class="metric-label">Bajet</span>
                                <span style="font-weight:bold; color:#2C7DA6;">{format_nilai(b)}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-label">Bajet Qtr</span>
                                <span style="font-weight:bold; color:#E08E4E;">{format_nilai(s)}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-label">Sebenar</span>
                                <span style="font-weight:bold; color:#2E8B6D;">{format_nilai(se)}</span>
                            </div>
                        </div>
                        """)

    with st.expander("📊 CARTA 1: PERBANDINGAN  KATEGORI", expanded=False):
        df_chart = df_akhir.copy()
        df_chart["BAJET_JT"] = df_chart["BAJET 2025"] / 1_000_000
        df_chart["SASARAN_JT"] = df_chart["SASARAN Q1-25"] / 1_000_000
        df_chart["SEBENAR_JT"] = df_chart["SEBENAR Q1-25"] / 1_000_000

        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_chart[df_chart["Quarter"] == q]
                df_c1 = df_q.groupby("Kategori", as_index=False).agg({
                    "BAJET_JT": "sum",
                    "SASARAN_JT": "sum",
                    "SEBENAR_JT": "sum"
                })
                with cols[i]:
                    st.markdown(f"**Tempoh {q}**")
                    fig = px.bar(
                        df_c1,
                        x="Kategori",
                        y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                        barmode="group",
                        height=620,
                        labels={
                            "Kategori": "Kategori",
                            "value": "Nilai",
                            "variable": "Jenis"
                        },
                        color_discrete_sequence=["#2C7DA6", "#E08E4E", "#2E8B6D"]
                    )
                    for trace in fig.data:
                        kemas_label_bajet(trace)
                        trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
                    apply_chart_text_style(fig, size=11, angle=-15)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            df_c1 = df_chart.groupby("Kategori", as_index=False).agg({
                "BAJET_JT": "sum",
                "SASARAN_JT": "sum",
                "SEBENAR_JT": "sum"
            })
            fig1 = px.bar(
                df_c1,
                x="Kategori",
                y=["BAJET_JT", "SASARAN_JT", "SEBENAR_JT"],
                barmode="group",
                height=650,
                labels={
                    "Kategori": "Kategori",
                    "value": "Nilai",
                    "variable": "Jenis"
                },
                color_discrete_sequence=["#2C7DA6", "#E08E4E", "#2E8B6D"]
            )
            for trace in fig1.data:
                kemas_label_bajet(trace)
                trace.text = [format_nilai(x * 1_000_000) for x in trace.y]
            apply_chart_text_style(fig1, size=12, angle=0)
            st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📊 CARTA 2: PERBANDINGAN SEBENAR 06-2026 VS 06-2025", expanded=False):
        # =======================
        # CARTA 2 - COMPARISON DALAM SATU FAIL EXCEL
        # Fail: JPKA_ANALISA PK CIDB 06-2026.xlsx
        # Column semasa : SEBENAR Q1-25 / SEBENAR 06-2026
        # Column sebelum: SEBENAR 06-2025
        # =======================
        df_compare = df_akhir.copy()

        if "SEBENAR 06-2025" not in df_compare.columns:
            st.warning("Column SEBENAR 06-2025 tidak dijumpai dalam data Excel.")
        else:
            nilai_2026 = pd.to_numeric(
                df_compare["SEBENAR Q1-25"],
                errors="coerce"
            ).fillna(0).sum()

            nilai_2025 = pd.to_numeric(
                df_compare["SEBENAR 06-2025"],
                errors="coerce"
            ).fillna(0).sum()

            df_total_chart = pd.DataFrame({
                "Tempoh": ["06-2025", "06-2026"],
                "Jumlah Sebenar": [nilai_2025, nilai_2026]
            })

            fig_total = px.bar(
                df_total_chart,
                x="Tempoh",
                y="Jumlah Sebenar",
                labels={
                    "Jumlah Sebenar": "Jumlah Sebenar (RM)",
                    "Tempoh": "Tempoh"
                },
                text=df_total_chart["Jumlah Sebenar"].apply(format_nilai)
            )

            warna_carta2 = ["#9CA3AF", "#2E8B6D"]

            fig_total.update_traces(
                marker_color=warna_carta2,
                text=df_total_chart["Jumlah Sebenar"].apply(format_nilai)
            )

            # DOTTED untuk bar tahun sebelum (06-2025)
            fig_total.update_traces(
                marker_pattern_shape=[".", ""],
                marker_pattern_fgcolor=["white", "rgba(0,0,0,0)"],
                marker_pattern_size=[7, 0],
                marker_pattern_solidity=[0.25, 0]
            )

            apply_chart_text_style(fig_total, size=12, angle=0)

            # =======================
            # NOTA PERBANDINGAN
            # Formula:
            # ((SEBENAR 06-2026 / SEBENAR 06-2025) * 100) - 100
            # =======================
            if nilai_2025 != 0:
                peratus_banding = (nilai_2026 / nilai_2025) * 100
                gauge_delta = peratus_banding - 100

                if gauge_delta > 0:
                    label_banding = f"+{gauge_delta:.0f}%"
                    warna_gauge = "#16a34a"
                    arah_label = "meningkat"
                elif gauge_delta < 0:
                    label_banding = f"{gauge_delta:.0f}%"
                    warna_gauge = "#dc2626"
                    arah_label = "menurun"
                else:
                    label_banding = "0%"
                    warna_gauge = "#f59e0b"
                    arah_label = "tiada perubahan"
            else:
                label_banding = "#DIV/0!"
                warna_gauge = "#64748b"
                arah_label = "tidak dapat dikira"

            y_max_chart = max(
                pd.to_numeric(df_total_chart["Jumlah Sebenar"], errors="coerce").fillna(0).max(),
                1
            )

            fig_total.add_annotation(
                x=0.5,
                y=y_max_chart * 1.14,
                xref="paper",
                yref="y",
                text=f"06-2026 berbanding 06-2025: {label_banding} ({arah_label})",
                showarrow=False,
                font=dict(
                    size=15,
                    color=warna_gauge,
                    family="Arial Black"
                ),
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor=warna_gauge,
                borderwidth=1.5,
                borderpad=8
            )

            fig_total.update_layout(
                height=650,
                xaxis_title="Tempoh",
                yaxis_title="Jumlah Sebenar (RM)",
                margin=dict(t=150, b=100, l=90, r=90),
                template="plotly_white"
            )

            st.plotly_chart(fig_total, use_container_width=True)

            df_compare_show = pd.DataFrame({
                "Perkara": [
                    "Sebenar 06-2025",
                    "Sebenar 06-2026",
                    "Perubahan RM",
                    "Perubahan %"
                ],
                "Nilai": [
                    format_comma(nilai_2025),
                    format_comma(nilai_2026),
                    format_comma(nilai_2026 - nilai_2025),
                    label_banding
                ]
            })

            st.dataframe(
                df_compare_show,
                use_container_width=True,
                hide_index=True
            )

    with st.expander("📊 CARTA 3: PRESTASI  ITEM", expanded=False):
        if len(pilih_quarter) > 1:
            cols = st.columns(len(pilih_quarter))
            for i, q in enumerate(pilih_quarter):
                df_q = df_akhir[df_akhir["Quarter"] == q]
                df_c2 = (
                    df_q.groupby("DESC", as_index=False)
                    .agg({"SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"})
                    .sort_values("SEBENAR Q1-25", ascending=False)
                    .head(20)
                )
                with cols[i]:
                    st.markdown(f"**Tempoh {q}**")
                    fig2 = px.bar(
                        df_c2,
                        y="DESC",
                        x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                        orientation="h",
                        barmode="group",
                        height=760,
                        labels={
                            "DESC": "Item",
                            "value": "Nilai",
                            "variable": "Jenis"
                        },
                        color_discrete_sequence=["#E08E4E", "#2E8B6D"]
                    )
                    for trace in fig2.data:
                        kemas_label_bajet(trace)
                        trace.text = [format_nilai(x) for x in trace.x]
                    apply_chart_text_style(fig2, size=10, angle=0)
                    max_x = max([max(list(t.x)) for t in fig2.data if len(list(t.x)) > 0]) if fig2.data else 0
                    fig2.update_layout(
                        yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()),
                        xaxis_range=[0, max_x * 1.25 if max_x else None]
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            df_c2 = (
                df_akhir.groupby("DESC", as_index=False)
                .agg({"SASARAN Q1-25": "sum", "SEBENAR Q1-25": "sum"})
                .sort_values("SEBENAR Q1-25", ascending=False)
                .head(20)
            )
            fig2 = px.bar(
                df_c2,
                y="DESC",
                x=["SASARAN Q1-25", "SEBENAR Q1-25"],
                orientation="h",
                barmode="group",
                height=760,
                labels={
                    "DESC": "Item",
                    "value": "Nilai",
                    "variable": "Jenis"
                },
                color_discrete_sequence=["#E08E4E", "#2E8B6D"]
            )
            for trace in fig2.data:
                kemas_label_bajet(trace)
                trace.text = [format_nilai(x) for x in trace.x]
            apply_chart_text_style(fig2, size=12, angle=0)
            max_x = max([max(list(t.x)) for t in fig2.data if len(list(t.x)) > 0]) if fig2.data else 0
            fig2.update_layout(
                yaxis=dict(categoryorder="array", categoryarray=df_c2["DESC"].tolist()),
                xaxis_range=[0, max_x * 1.25 if max_x else None]
            )
            st.plotly_chart(fig2, use_container_width=True)



    with st.expander("📊 CARTA 4: KOD ITEM", expanded=False):
        df_by_kod_item = (
            df_akhir.groupby(["KOD1"], as_index=False)
            .agg({
                "SEBENAR Q1-25": "sum"
            })
        )

        df_by_kod_item["SEBENAR_JT"] = df_by_kod_item["SEBENAR Q1-25"] / 1_000_000

        df_by_kod_item = (
            df_by_kod_item
            .sort_values("SEBENAR Q1-25", ascending=False)
            .head(25)
        )

        # Warna selang-seli soft & pekat ala 3D corporate
        warna_bars_kod_item = []
        for i in range(len(df_by_kod_item)):
            if i % 2 == 0:
                warna_bars_kod_item.append("rgba(125,211,252,0.78)")  # soft blue
            else:
                warna_bars_kod_item.append("rgba(14,165,233,0.95)")   # deep blue

        fig_by_kod_item = px.bar(
            df_by_kod_item,
            y="KOD1",
            x="SEBENAR_JT",
            orientation="h",
            height=850,
            text=df_by_kod_item["SEBENAR Q1-25"].apply(format_nilai),
            labels={
                "KOD1": "Kod Item",
                "SEBENAR_JT": "Sebenar"
            }
        )

        fig_by_kod_item.update_traces(
            marker_color=warna_bars_kod_item
        )

        fig_by_kod_item.update_traces(
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(
                size=11,
                color="#0f172a",
                family="Arial Black"
            ),
            marker=dict(
                line=dict(
                    color="rgba(255,255,255,0.78)",
                    width=1.5
                )
            ),
            opacity=0.96,
            name="Sebenar",

            # effect ala 3D/glow
            hovertemplate="<b>%{y}</b><br>Sebenar: %{text}<extra></extra>"
        )

        max_x_kod_item = (
            df_by_kod_item["SEBENAR_JT"].max()
            if not df_by_kod_item.empty
            else 0
        )

        fig_by_kod_item.update_layout(
            title=" ",
            yaxis=dict(
                categoryorder="array",
                categoryarray=df_by_kod_item["KOD1"].tolist()
            ),
            xaxis_range=[0, max_x_kod_item * 1.30 if max_x_kod_item else None],
            xaxis_title="Sebenar",
            yaxis_title="Kod Item",
            legend_title_text="Jenis",
            template="plotly_white",
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(241,245,249,0.82)",
            font=dict(
                family="Arial",
                color="#334155"
            ),
            title_font=dict(
                size=22,
                color="#0f172a",
                family="Arial Black"
            ),
            margin=dict(t=120, b=120, l=180, r=120),
            showlegend=False
        )

        st.plotly_chart(fig_by_kod_item, use_container_width=True)

    with st.expander("📈 CARTA 5: PRESTASI PTJ", expanded=False):

        df_c6 = df_group.copy()

        df_c6["BAJET 2025"] = pd.to_numeric(
            df_c6["BAJET 2025"],
            errors="coerce"
        ).fillna(0)

        df_c6["SASARAN Q1-25"] = pd.to_numeric(
            df_c6["SASARAN Q1-25"],
            errors="coerce"
        ).fillna(0)

        df_c6["SEBENAR Q1-25"] = pd.to_numeric(
            df_c6["SEBENAR Q1-25"],
            errors="coerce"
        ).fillna(0)

        # Line merah = Pencapaian (%) pada axis kanan.
        df_c6["% Pencapaian"] = df_c6.apply(
            lambda row: None
            if row["SASARAN Q1-25"] <= 0
            else hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )

        # Bar hijau = Jumlah Sebenar.
        df_c6["Jumlah Sebenar"] = df_c6["SEBENAR Q1-25"]

        # Line kuning = Nilai Sasaran, bukan peratus.
        df_c6["Jumlah Sasaran"] = df_c6["SASARAN Q1-25"]

        # =====================================================
        # SORT CARTA 6
        # Lebih stabil daripada klik legend untuk hide/show.
        # User boleh pilih nilai yang mahu dijadikan asas susunan.
        # =====================================================
        sort_col_c6a, sort_col_c6b = st.columns([2, 1])

        with sort_col_c6a:
            sort_carta6 = st.radio(
                "Sort Carta 6 ikut",
                [
                    "Jumlah Sebenar",
                    "Sasaran Nilai",
                    "Pencapaian (%)"
                ],
                horizontal=True,
                key="sort_carta6_belanja_hasil"
            )

        with sort_col_c6b:
            sort_desc_c6 = st.toggle(
                "Descending",
                value=True,
                key="sort_desc_carta6_belanja_hasil"
            )

        sort_column_map_c6 = {
            "Jumlah Sebenar": "Jumlah Sebenar",
            "Sasaran Nilai": "Jumlah Sasaran",
            "Pencapaian (%)": "% Pencapaian"
        }

        df_c6 = df_c6.sort_values(
            by=sort_column_map_c6.get(sort_carta6, "Jumlah Sebenar"),
            ascending=not sort_desc_c6,
            na_position="last"
        ).reset_index(drop=True)

        fig6 = go.Figure()

        # Bar Hijau = Jumlah Sebenar, axis kiri.
        fig6.add_trace(go.Bar(
            x=df_c6["PTJ1"],
            y=df_c6["Jumlah Sebenar"],
            name="Jumlah Sebenar",
            marker_color="#8ED04F",
            text=df_c6["Jumlah Sebenar"].apply(short_number),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                size=11,
                color="black",
                family="Arial"
            ),
            yaxis="y",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Jumlah Sebenar: %{text}<br>"
                "<extra></extra>"
            )
        ))

        # Line Kuning = Jumlah Sasaran, axis kiri.
        fig6.add_trace(go.Scatter(
            x=df_c6["PTJ1"],
            y=df_c6["Jumlah Sasaran"],
            name="Sasaran Nilai",
            line=dict(color="#FFB000", width=3, dash="dash"),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c6["Jumlah Sasaran"].apply(short_number),
            textposition="top center",
            textfont=dict(
                size=10,
                color="black",
                family="Arial"
            ),
            yaxis="y",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sasaran Nilai: %{text}<br>"
                "<extra></extra>"
            )
        ))

        # Line Merah = Pencapaian %, axis kanan.
        fig6.add_trace(go.Scatter(
            x=df_c6["PTJ1"],
            y=df_c6["% Pencapaian"],
            name="Pencapaian (%)",
            line=dict(color="red", width=4),
            marker=dict(size=7),
            mode="lines+markers+text",
            text=df_c6["% Pencapaian"].apply(
                lambda x: "" if pd.isna(x) else f"{x:.0f}%"
            ),
            textposition="top center",
            textfont=dict(
                size=10,
                color="black",
                family="Arial"
            ),
            yaxis="y2",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Pencapaian: %{y:.2f}%<br>"
                "<extra></extra>"
            )
        ))

        left_max = max(
            pd.to_numeric(df_c6["Jumlah Sebenar"], errors="coerce").max(),
            pd.to_numeric(df_c6["Jumlah Sasaran"], errors="coerce").max()
        )

        right_max = pd.to_numeric(
            df_c6["% Pencapaian"],
            errors="coerce"
        ).max()

        fig6.update_layout(
            height=780,
            template="plotly_white",
            xaxis=dict(
                title="PTJ",
                tickangle=-45,
                automargin=True
            ),
            yaxis=dict(
                title="Jumlah / Sasaran (RM)",
                range=[0, left_max * 1.20 if left_max else 1],
                tickformat=",.0f"
            ),
            yaxis2=dict(
                title="Pencapaian (%)",
                overlaying="y",
                side="right",
                ticksuffix="%",
                range=[0, right_max * 1.20 if right_max else 100],
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=120, b=180, l=90, r=90)
        )

        fig6.update_traces(
            cliponaxis=False
        )

        st.plotly_chart(fig6, use_container_width=True)


    with st.expander("📋 SUMMARY KESELURUHAN", expanded=False):
        summary = df_akhir.groupby(["PTJ1", "Kategori", "DESC", "Quarter"], as_index=False).agg({
            "BAJET 2025": "sum",
            "SASARAN Q1-25": "sum",
            "SEBENAR Q1-25": "sum",
            "SEBENAR 06-2025": "sum"
        })
        summary["Prestasi_%"] = summary.apply(
            lambda row: hitung_prestasi(row["SEBENAR Q1-25"], row["SASARAN Q1-25"]),
            axis=1
        )
        summary = summary.round(2)
        summary = rename_summary_columns(summary)

        # Tambah row JUMLAH di bawah sekali.
        # Belanja & Hasil: jumlahkan semua nilai Bajet, Sasaran dan Sebenar.
        jumlah_summary = {
            "PTJ": "JUMLAH",
            "Kategori": "",
            "Item": "",
            "Tempoh": "",
            "Bajet": pd.to_numeric(summary["Bajet"], errors="coerce").fillna(0).sum(),
            "Bajet Qtr": pd.to_numeric(summary["Bajet Qtr"], errors="coerce").fillna(0).sum(),
            "Sebenar 06-2026": pd.to_numeric(summary["Sebenar 06-2026"], errors="coerce").fillna(0).sum(),
            "Sebenar 06-2025": pd.to_numeric(summary["Sebenar 06-2025"], errors="coerce").fillna(0).sum(),
            "Prestasi_%": hitung_prestasi(
                pd.to_numeric(summary["Sebenar 06-2026"], errors="coerce").fillna(0).sum(),
                pd.to_numeric(summary["Bajet Qtr"], errors="coerce").fillna(0).sum()
            )
        }

        summary = pd.concat(
            [summary, pd.DataFrame([jumlah_summary])],
            ignore_index=True
        )

        # Paparan summary dengan comma style pada semua nilai numeric.
        summary_show = dataframe_comma_style(
            summary,
            money_cols=["Bajet", "Bajet Qtr", "Sebenar 06-2026", "Sebenar 06-2025"],
            percent_cols=["Prestasi_%"]
        )

        st.dataframe(
            summary_show,
            use_container_width=True,
            hide_index=True
        )

        # Download kekal raw numeric supaya masih boleh dikira dalam Excel.
        excel_file = to_excel(summary)
        st.download_button(
            "📥 Download Summary sebagai Excel",
            data=excel_file,
            file_name=f"Summary_CIDB_{'_'.join(pilih_quarter)}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.caption("Tempoh: 06-2026 • Comparison Carta 2 menggunakan column SEBENAR 06-2025 • Prestasi Kewangan CIDB JPKA")

# =======================
# MENU 2: GERAN - SLICER DARI WORKSHEET DATA COLUMN NAMA DAN LEGEND
# =======================
elif menu == "2. Geran":
    st.markdown("## 🧾 MODUL GERAN")
    if df_geran.empty:
        st.error("Data Geran tidak berjaya dimuatkan.")
        if geran_error:
            st.info(geran_error)
        st.stop()

    df_geran_work = df_geran.copy()

    nama_col = "NAMA"
    nama_short_col = "NAMA1"
    legend_col = "LEGEND"
    ptj_col = "PTJ"

    if nama_col not in df_geran_work.columns:
        st.error("Column NAMA tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if nama_short_col not in df_geran_work.columns:
        st.error("Column NAMA1 tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if legend_col not in df_geran_work.columns:
        st.error("Column LEGEND tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    if ptj_col not in df_geran_work.columns:
        st.error("Column PTJ tidak dijumpai dalam worksheet DATA.")
        st.write("Column yang ada:", df_geran_work.columns.tolist())
        st.stop()

    amount_col = detect_amount_column(df_geran_work)
    if amount_col is not None:
        df_geran_work[amount_col] = clean_numeric_series(df_geran_work[amount_col])
        # Dalam fail GL Q2, PERBELANJAAN dan BAYAR BALIK direkod sebagai negatif.
        # Tukar kepada amaun positif untuk paparan; formula baki tetap menolaknya.
        legend_norm = df_geran_work["LEGEND"].fillna("").astype(str).str.strip().str.upper()
        mask_out = legend_norm.isin(["PERBELANJAAN", "BYR BALIK", "BAYAR BALIK"])
        df_geran_work.loc[mask_out, amount_col] = df_geran_work.loc[mask_out, amount_col].abs()
        df_geran_work.loc[~mask_out, amount_col] = df_geran_work.loc[~mask_out, amount_col].clip(lower=0)

    df_geran_tapis = df_geran_work.copy()

    # =======================
    # PILLS + TICK SLICER ENGINE
    # GERAN - SAMA BENTUK & FUNCTION DENGAN BELANJA & HASIL
    #
    # Konsep:
    # - Semua slicer dalam expander.
    # - Pilihan selected dipaparkan dengan ✅.
    # - Pilihan belum selected dipaparkan dengan ◻️.
    # - Klik pill = toggle pilih/buang.
    # - Empty selected = ALL.
    # - Options setiap slicer dikira berdasarkan filter lain.
    # =======================

    def _geran_as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def _geran_unique_col(df_source, col):
        if col not in df_source.columns:
            return []
        return unique_sorted(df_source[col])

    def _geran_filter_df(df_source, filters, exclude_col=None):
        df_temp = df_source.copy()

        for col, vals in filters.items():
            if exclude_col is not None and col == exclude_col:
                continue

            vals = _geran_as_list(vals)
            if vals and col in df_temp.columns:
                df_temp = df_temp[
                    df_temp[col].astype(str).isin(vals)
                ]

        return df_temp

    def _get_geran_filter_state():
        return {
            ptj_col: _geran_as_list(st.session_state.get("geran_ptj_final2", [])),
            nama_col: _geran_as_list(st.session_state.get("geran_nama_final2", [])),
            legend_col: _geran_as_list(st.session_state.get("geran_legend_final2", [])),
        }

    def _set_geran_filter_value(col, values):
        values = _geran_as_list(values)

        if col == ptj_col:
            st.session_state["geran_ptj_final2"] = values
        elif col == nama_col:
            st.session_state["geran_nama_final2"] = values
        elif col == legend_col:
            st.session_state["geran_legend_final2"] = values

    def _clean_geran_filter_values(df_source):
        filters = _get_geran_filter_state()

        for col, vals in filters.items():
            valid = set(_geran_unique_col(df_source, col))
            cleaned = [
                x for x in _geran_as_list(vals)
                if x in valid
            ]
            _set_geran_filter_value(col, cleaned)

    def _geran_options_for_slicer(df_source, col):
        filters = _get_geran_filter_state()
        df_context = _geran_filter_df(
            df_source,
            filters,
            exclude_col=col
        )
        return _geran_unique_col(df_context, col)

    def _geran_pill_label(value, selected_values):
        selected_set = set(_geran_as_list(selected_values))
        return f"✅ {value}" if value in selected_set else f"◻️ {value}"

    def _geran_remove_tick_icon(label):
        label = str(label)
        label = label.replace("✅ ", "", 1)
        label = label.replace("◻️ ", "", 1)
        return label.strip()

    def _sync_geran_pill_toggle(col, pill_key, selected_key):
        raw_clicked = _geran_as_list(st.session_state.get(pill_key, []))
        if not raw_clicked:
            return

        clicked_values = [
            _geran_remove_tick_icon(x)
            for x in raw_clicked
        ]

        current_selected = _geran_as_list(
            st.session_state.get(selected_key, [])
        )
        selected_set = set(current_selected)

        for value in clicked_values:
            if value in selected_set:
                selected_set.remove(value)
            else:
                selected_set.add(value)

        st.session_state[selected_key] = sorted(list(selected_set))
        st.session_state[f"{selected_key}_expanded"] = True
        st.session_state[pill_key] = []

    def _render_geran_pill_slicer(
        title,
        col,
        selected_key,
        pill_key,
        df_source
    ):
        options = _geran_options_for_slicer(df_source, col)

        current_selected = [
            x for x in _geran_as_list(
                st.session_state.get(selected_key, [])
            )
            if x in set(options)
        ]
        st.session_state[selected_key] = current_selected

        if current_selected:
            expander_title = (
                f"{title}  ✅ {len(current_selected)}/{len(options)}"
            )
        else:
            expander_title = f"{title}  🌐 All ({len(options)})"

        expanded_key = f"{selected_key}_expanded"

        with st.expander(
            expander_title,
            expanded=st.session_state.get(expanded_key, False)
        ):
            if current_selected:
                st.caption(
                    f"Selected: {len(current_selected)} / {len(options)}"
                )
            else:
                st.caption(
                    f"All selected secara automatik: {len(options)} item"
                )

            pill_options = [
                _geran_pill_label(x, current_selected)
                for x in options
            ]

            st.pills(
                title,
                options=pill_options,
                selection_mode="multi",
                key=pill_key,
                label_visibility="collapsed",
                on_change=lambda: _sync_geran_pill_toggle(
                    col,
                    pill_key,
                    selected_key
                )
            )

    with st.sidebar:
        st.markdown("### 🔎 PILIHAN GERAN")

        df_geran_slicer_base = df_geran_tapis.copy()

        geran_selected_keys = [
            "geran_ptj_final2",
            "geran_nama_final2",
            "geran_legend_final2",
        ]

        for key in geran_selected_keys:
            if key not in st.session_state:
                st.session_state[key] = []

        _clean_geran_filter_values(df_geran_slicer_base)

        _render_geran_pill_slicer(
            "⚡ Pilih PTJ",
            ptj_col,
            "geran_ptj_final2",
            "geran_ptj_pills_tick",
            df_geran_slicer_base
        )

        _render_geran_pill_slicer(
            "🏢 Pilih NAMA",
            nama_col,
            "geran_nama_final2",
            "geran_nama_pills_tick",
            df_geran_slicer_base
        )

        _render_geran_pill_slicer(
            "📂 Pilih LEGEND",
            legend_col,
            "geran_legend_final2",
            "geran_legend_pills_tick",
            df_geran_slicer_base
        )

        geran_active_count = sum(
            1 for vals in _get_geran_filter_state().values()
            if _geran_as_list(vals)
        )
        st.caption(f"Filter aktif: {geran_active_count}/3")

        if st.button(
            "♻️ Reset Slicer Geran",
            key="reset_slicer_geran_final2"
        ):
            for key in [
                "geran_ptj_final2",
                "geran_nama_final2",
                "geran_legend_final2",
                "geran_ptj_pills_tick",
                "geran_nama_pills_tick",
                "geran_legend_pills_tick",
                "geran_ptj_final2_expanded",
                "geran_nama_final2_expanded",
                "geran_legend_final2_expanded",
                # Bersihkan state geran lama supaya tidak mengganggu.
                "geran_ptj_final",
                "geran_nama_final",
                "geran_legend_final",
                "geran_ptj_pills_multi",
                "geran_nama_pills_multi",
                "geran_legend_pills_multi",
                "geran_stable_slicer_initialized",
                "_geran_prev_ptj",
                "_geran_prev_nama",
                "_geran_prev_legend",
                "_geran_force_pills_ptj",
                "_geran_force_pills_nama",
                "_geran_force_pills_legend",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    pilih_ptj_geran = _geran_as_list(st.session_state.get("geran_ptj_final2", []))
    pilih_nama = _geran_as_list(st.session_state.get("geran_nama_final2", []))
    pilih_legend = _geran_as_list(st.session_state.get("geran_legend_final2", []))

    active_filters_geran = {
        ptj_col: pilih_ptj_geran,
        nama_col: pilih_nama,
        legend_col: pilih_legend,
    }

    # Empty selection = ALL, sama seperti Belanja & Hasil.
    df_geran_tapis = _geran_filter_df(
        df_geran_tapis,
        active_filters_geran
    )

    if df_geran_tapis.empty:
        st.warning("Tiada data Geran selepas tapisan dibuat.")
        st.stop()

    # KPI Geran:
    # Column LEGEND menentukan kategori:
    # - PEMBERIAN
    # - PERBELANJAAN
    # - BYR BALIK
    # Nilai dikira menggunakan column "Amount in local currency"
    if amount_col is None:
        st.error("Column Amount in local currency / amaun tidak dijumpai untuk kira KPI Geran.")
        st.stop()

    legend_upper = df_geran_tapis[legend_col].astype(str).str.strip().str.upper()

    jumlah_pemberian = df_geran_tapis.loc[
        legend_upper.eq("PEMBERIAN"),
        amount_col
    ].sum()

    jumlah_perbelanjaan = df_geran_tapis.loc[
        legend_upper.eq("PERBELANJAAN"),
        amount_col
    ].sum()

    jumlah_bayar_balik = df_geran_tapis.loc[
        legend_upper.isin(["BYR BALIK", "BAYAR BALIK"]),
        amount_col
    ].sum()

    # KPI Baki Geran = Pemberian - Perbelanjaan - Bayar Balik
    baki_geran = (
        jumlah_pemberian
        - jumlah_perbelanjaan
        - jumlah_bayar_balik
    )

    col_g1, col_g2, col_g3, col_g4 = st.columns(4)

    with col_g1:
        st.metric("Jumlah Pemberian", format_nilai(jumlah_pemberian))

    with col_g2:
        st.metric("Jumlah Perbelanjaan", format_nilai(jumlah_perbelanjaan))

    with col_g3:
        st.metric("Jumlah Bayar Balik", format_nilai(jumlah_bayar_balik))

    with col_g4:
        st.metric("BAKI GERAN", format_nilai(baki_geran))

    # =======================
    # DATA UNTUK CARTA GERAN
    # =======================
    if amount_col is None:
        st.error("Column Amount in local currency / amaun tidak dijumpai untuk bina Carta Geran.")
        st.stop()

    # CARTA 1:
    # NAMA vs PEMBERIAN, PERBELANJAAN dan BYR BALIK.
    # Nilai negatif diabaikan.
    df_chart_geran = df_geran_tapis.copy()
    df_chart_geran[amount_col] = clean_numeric_series(df_chart_geran[amount_col])
    df_chart_geran = df_chart_geran[df_chart_geran[amount_col] >= 0].copy()
    df_chart_geran["_LEGEND_UPPER"] = df_chart_geran[legend_col].astype(str).str.strip().str.upper()

    df_chart_geran = df_chart_geran[
        df_chart_geran["_LEGEND_UPPER"].isin(["PEMBERIAN", "PERBELANJAAN", "BYR BALIK", "BAYAR BALIK"])
    ].copy()

    df_chart_geran["_LEGEND_UPPER"] = df_chart_geran["_LEGEND_UPPER"].replace({
        "BAYAR BALIK": "BYR BALIK"
    })

    df_nama_legend = (
        df_chart_geran
        .pivot_table(
            index=nama_short_col,
            columns="_LEGEND_UPPER",
            values=amount_col,
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    for col in ["PEMBERIAN", "PERBELANJAAN", "BYR BALIK"]:
        if col not in df_nama_legend.columns:
            df_nama_legend[col] = 0

    df_nama_legend["Jumlah"] = (
        df_nama_legend["PEMBERIAN"]
        + df_nama_legend["PERBELANJAAN"]
        + df_nama_legend["BYR BALIK"]
    )

    df_nama_legend["BAKI GERAN"] = (
        df_nama_legend["PEMBERIAN"]
        - df_nama_legend["PERBELANJAAN"]
        - df_nama_legend["BYR BALIK"]
    )

    df_nama_legend = df_nama_legend.sort_values("Jumlah", ascending=False)

    # =======================
    # CARTA 1
    # =======================
    fig_geran_nama = px.bar(
        df_nama_legend,
        x=nama_short_col,
        y=["PEMBERIAN", "PERBELANJAAN", "BYR BALIK"],
        barmode="group",
        title=" ",
        labels={
            "value": "Jumlah",
            "variable": "Jenis",
            nama_short_col: "NAMA1"
        },
        height=600,
        color_discrete_map={
            "PEMBERIAN": "#f6d365",
            "PERBELANJAAN": "#f4978e",
            "BYR BALIK": "#95d5b2"
        }
    )

    warna_trace = {
        "PEMBERIAN": "#f6d365",
        "PERBELANJAAN": "#f4978e",
        "BYR BALIK": "#95d5b2"
    }

    for trace in fig_geran_nama.data:
        trace.text = [format_nilai(x) for x in trace.y]

        if trace.name in warna_trace:
            trace.marker.color = warna_trace[trace.name]

    apply_chart_text_style(fig_geran_nama, size=11, angle=0)

    fig_geran_nama.update_layout(
        xaxis_title=" ",
        xaxis_tickangle=-45,
        yaxis_title="Jumlah",
        legend_title_text="Jenis",
        template="plotly_white"
    )

    # =======================
    # CARTA 2
    # Baki Geran = PEMBERIAN - PERBELANJAAN - BYR BALIK
    # =======================
    df_baki_geran = df_nama_legend.copy()
    df_baki_geran = df_baki_geran.sort_values("BAKI GERAN", ascending=False)

    fig_baki = px.bar(
        df_baki_geran,
        x=nama_short_col,
        y="BAKI GERAN",
        text=df_baki_geran["BAKI GERAN"].apply(format_nilai),
        title=" ",
        color_discrete_sequence=["#bde0fe"]
    )

    apply_chart_text_style(fig_baki, size=11, angle=0)

    fig_baki.update_layout(
        height=600,
        xaxis_title=" ",
        xaxis_tickangle=-45,
        yaxis_title="Baki Geran",
        template="plotly_white"
    )

    # =======================
    # PAPAR CARTA 1 DAN 2 BERSEBELAHAN
    # =======================
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### 📊 Carta 1: Geran")

        # Sembunyikan bar yang nilainya 0.
        try:
            for trace in fig_geran_nama.data:
                if getattr(trace, "type", "") == "bar":
                    vals = list(trace.y) if getattr(trace, "orientation", None) != "h" else list(trace.x)

                    # Tukar nilai 0 kepada None supaya bar tidak dipaparkan.
                    vals_filtered = [
                        None if pd.to_numeric(v, errors="coerce") == 0 else v
                        for v in vals
                    ]

                    if getattr(trace, "orientation", None) == "h":
                        trace.x = vals_filtered
                    else:
                        trace.y = vals_filtered

        except Exception:
            pass

        fig_geran_nama = apply_geran_arrow_labels(
            fig_geran_nama,
            orientation="v",
            threshold_ratio=0.18
        )

        st.plotly_chart(
            fig_geran_nama,
            use_container_width=True
        )

    with col_chart2:
        st.markdown("### 📊 Carta 2: Baki Geran")
        st.plotly_chart(
            fig_baki,
            use_container_width=True
        )

    # =======================
    # CARTA 3 GERAN -  PTJ
    # =======================
    st.markdown("### 📊 Carta 3: Prestasi  PTJ")

    if ptj_col in df_chart_geran.columns:

        df_ptj = (
            df_chart_geran
            .groupby([ptj_col, "_LEGEND_UPPER"], as_index=False)[amount_col]
            .sum()
        )

        fig_ptj = px.bar(
            df_ptj,
            x=ptj_col,
            y=amount_col,
            color="_LEGEND_UPPER",
            barmode="group",
            labels={
                ptj_col: "PTJ",
                amount_col: "Jumlah",
                "_LEGEND_UPPER": "Jenis"
            },
            height=650,
            color_discrete_map={
                "PEMBERIAN": "#f6d365",
                "PERBELANJAAN": "#f4978e",
                "BYR BALIK": "#95d5b2"
            }
        )

        for trace in fig_ptj.data:
            trace.text = [format_nilai(x) for x in trace.y]

            if trace.name in warna_trace:
                trace.marker.color = warna_trace[trace.name]

        apply_chart_text_style(fig_ptj, size=11, angle=0)

        fig_ptj.update_layout(
            xaxis_tickangle=-45,
            template="plotly_white",
            yaxis_title="Jumlah",
            legend_title_text="Jenis"
        )

        st.plotly_chart(
            fig_ptj,
            use_container_width=True
        )

    else:
        st.warning("Column PTJ tidak dijumpai dalam data Geran.")

    # =======================
    # DATA GERAN  SUSUNAN EXCEL
    # Susunan column:
    # PTJ | NAMA | LEGEND | JUMLAH
    # =======================
    df_data_carta_geran_gabung = (
        df_chart_geran
        .groupby([ptj_col, nama_col, legend_col], as_index=False)[amount_col]
        .sum()
        .rename(columns={
            ptj_col: "PTJ",
            nama_col: "NAMA",
            legend_col: "LEGEND",
            amount_col: "JUMLAH"
        })
    )

    # Kekalkan susunan column seperti Excel
    df_data_carta_geran_gabung = df_data_carta_geran_gabung[
        ["PTJ", "NAMA", "LEGEND", "JUMLAH"]
    ]

    # Susunan row ikut Excel: PTJ -> NAMA -> LEGEND
    df_data_carta_geran_gabung = df_data_carta_geran_gabung.sort_values(
        by=["PTJ", "NAMA", "LEGEND"],
        ascending=[True, True, True]
    ).reset_index(drop=True)

    # Tambah row JUMLAH di bawah sekali.
    # Geran: JUMLAH = PEMBERIAN - PERBELANJAAN - BAYAR BALIK.
    legend_total_upper = df_chart_geran[legend_col].astype(str).str.strip().str.upper()
    jumlah_pemberian_data = df_chart_geran.loc[
        legend_total_upper.eq("PEMBERIAN"),
        amount_col
    ].sum()
    jumlah_perbelanjaan_data = df_chart_geran.loc[
        legend_total_upper.eq("PERBELANJAAN"),
        amount_col
    ].sum()
    jumlah_bayar_balik_data = df_chart_geran.loc[
        legend_total_upper.isin(["BYR BALIK", "BAYAR BALIK"]),
        amount_col
    ].sum()

    jumlah_bersih_geran = (
        jumlah_pemberian_data
        - jumlah_perbelanjaan_data
        - jumlah_bayar_balik_data
    )

    df_data_carta_geran_gabung = pd.concat(
        [
            df_data_carta_geran_gabung,
            pd.DataFrame([{
                "PTJ": "JUMLAH",
                "NAMA": "",
                "LEGEND": "PEMBERIAN - PERBELANJAAN - BAYAR BALIK",
                "JUMLAH": jumlah_bersih_geran
            }])
        ],
        ignore_index=True
    )

    with st.expander("📄 DATA CARTA GERAN", expanded=False):
        df_data_carta_geran_show = dataframe_comma_style(
            df_data_carta_geran_gabung,
            money_cols=["JUMLAH"]
        )

        st.dataframe(
            df_data_carta_geran_show,
            use_container_width=True,
            hide_index=True
        )

        # Download kekal raw numeric dalam satu sheet sahaja.
        excel_data_carta = to_excel(
            df_data_carta_geran_gabung,
            sheet_name="DATA_CARTA_GERAN"
        )

        st.download_button(
            "📥 Download Data Carta Geran",
            data=excel_data_carta,
            file_name="Data_Carta_Geran.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# =======================
# MENU LAIN
# =======================
elif menu == "3. P&L":

    with st.sidebar:
        st.markdown("### 🔎  P&L")
        pilihan_pl = st.radio(
            "Pilih Paparan",
            [
                "Prestasi Hasil & Belanja CIDB",
                "Pecahan Belanja CIDB",
                "Surplus/(Defisit) Prestasi Bajet CIDB"
            ],
            index=0
        )

    # =======================
    # P&L - DATA RASMI JADUAL 6
    # Rujukan: 4.0 PRESTASI KEWANGAN CIDB
    # Jadual 6: Ringkasan Hasil dan Perbelanjaan Sehingga Suku Kedua 2026
    # =======================

    def kira_prestasi(sebenar, asas):
        sebenar = pd.to_numeric(sebenar, errors="coerce")
        asas = pd.to_numeric(asas, errors="coerce")
        if pd.isna(sebenar) or pd.isna(asas) or asas == 0:
            return None
        return (sebenar / asas) * 100

    def label_pct(nilai):
        nilai = pd.to_numeric(nilai, errors="coerce")
        if pd.isna(nilai):
            return "-"
        return f"{nilai:.0f}%"

    def format_juta_2(nilai):
        nilai = pd.to_numeric(nilai, errors="coerce")
        if pd.isna(nilai):
            nilai = 0
        return f"{nilai / 1_000_000:,.2f}"

    df_pl_jadual6 = pd.DataFrame({
        "PERKARA": [
            "Hasil",
            "Belanja program industri",
            "Belanja mengurus",
            "Jumlah perbelanjaan operasi",
            "Untung sebelum cukai dan zakat",
            "Cukai",
            "Zakat",
            "Untung selepas cukai dan zakat",
            "Belanja Modal",
            "Jumlah Perbelanjaan",
            "Lebihan/(Kurangan) Pendapatan Termasuk S/Nilai & H.Ragu",
            "(-) S/Nilai & H. Ragu",
            "Lebihan/(Kurangan) Pendapatan Tidak Termasuk S/Nilai & H.Ragu",
        ],
        "BAJET 2026": [
            485_000_000, 205_000_000, 189_000_000, 394_000_000,
            91_000_000, 8_000_000, 1_000_000, 82_000_000,
            91_000_000, 485_000_000, 0, 24_600_000, 24_600_000,
        ],
        "BAJET 06-2026": [
            239_500_000, 75_200_000, 78_853_000, 154_053_000,
            85_447_000, 0, 0, 85_447_000,
            11_845_000, 165_898_000, 73_602_000, 13_502_500, 87_104_500,
        ],
        "SEBENAR 06-2026": [
            281_306_655, 71_481_260, 72_733_800, 144_215_060,
            137_091_595, 0, 0, 137_091_595,
            10_539_572, 154_754_633, 126_552_022, 12_233_703, 138_785_725,
        ],
        "SEBENAR 06-2025": [
            248_235_126, 70_191_199, 68_704_605, 138_895_804,
            109_339_322, 0, 0, 109_339_322,
            5_938_709, 144_834_514, 103_400_612, 11_635_486, 115_036_098,
        ],
    })

    # Kira peratus ikut formula Jadual 6.
    df_pl_jadual6["Prestasi Bajet 06-2026"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 06-2026"], row["BAJET 06-2026"]),
        axis=1
    )
    df_pl_jadual6["Prestasi Bajet 2026"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 06-2026"], row["BAJET 2026"]),
        axis=1
    )
    df_pl_jadual6["Prestasi 06-26 vs 06-25"] = df_pl_jadual6.apply(
        lambda row: kira_prestasi(row["SEBENAR 06-2026"], row["SEBENAR 06-2025"]),
        axis=1
    )

    # Paparan utama P&L: Hasil, Jumlah Perbelanjaan dan lebihan.
    df_pl = pd.DataFrame({
        "PERKARA": [
            "HASIL",
            "JUMLAH PERBELANJAAN",
            "LEBIHAN/(KURANGAN) PENDAPATAN TIDAK TERMASUK S/NILAI & H.RAGU"
        ],
        "BAJET 2026": [485_000_000, 485_000_000, 24_600_000],
        "BAJET 06-2026": [239_500_000, 165_898_000, 87_104_500],
        "SEBENAR 06-2026": [281_306_655, 154_754_633, 138_785_725],
        "SEBENAR 06-2025": [248_235_126, 144_834_514, 115_036_098],
    })

    df_pecahan_belanja = pd.DataFrame({
        "KATEGORI": ["Belanja program industri", "Belanja mengurus", "Belanja Modal"],
        "BAJET 2026": [205_000_000, 189_000_000, 91_000_000],
        "BAJET 06-2026": [75_200_000, 78_853_000, 11_845_000],
        "SEBENAR 06-2026": [71_481_260, 72_733_800, 10_539_572],
        "SEBENAR 06-2025": [70_191_199, 68_704_605, 5_938_709],
        "Prestasi Bajet 06-2026": [95, 92, 89],
        "Prestasi Bajet 2026": [35, 38, 12],
        "Prestasi 06-26 vs 06-25": [102, 106, 177],
    })

    # =======================
    # KPI RINGKAS
    # =======================
    hasil_row = df_pl[df_pl["PERKARA"] == "HASIL"].iloc[0]
    belanja_row = df_pl[df_pl["PERKARA"] == "JUMLAH PERBELANJAAN"].iloc[0]
    lebihan_row = df_pl[df_pl["PERKARA"].str.contains("LEBIHAN", na=False)].iloc[0]

    col_pl1, col_pl2, col_pl3, col_pl4 = st.columns(4)
    with col_pl1:
        st.metric(
            "Hasil Sebenar 06-2026",
            format_nilai(hasil_row["SEBENAR 06-2026"]),
            f'{label_pct(kira_prestasi(hasil_row["SEBENAR 06-2026"], hasil_row["BAJET 06-2026"]))} vs Bajet 06-2026'
        )
    with col_pl2:
        st.metric(
            "Jumlah Perbelanjaan",
            format_nilai(belanja_row["SEBENAR 06-2026"]),
            f'{label_pct(kira_prestasi(belanja_row["SEBENAR 06-2026"], belanja_row["BAJET 06-2026"]))} vs Bajet 06-2026'
        )
    with col_pl3:
        st.metric(
            "Lebihan Pendapatan",
            format_nilai(lebihan_row["SEBENAR 06-2026"]),
            f'{format_nilai(lebihan_row["SEBENAR 06-2026"] - lebihan_row["SEBENAR 06-2025"])} vs 06-2025'
        )
    with col_pl4:
        st.metric(
            "Untung Selepas Cukai & Zakat",
            format_nilai(137_091_595),
            f'{format_nilai(137_091_595 - 109_339_322)} vs 06-2025'
        )

    st.markdown(f"### 📊 {pilihan_pl}")

    if pilihan_pl == "Prestasi Hasil & Belanja CIDB":

        df_chart_pl = df_pl[
            df_pl["PERKARA"].isin(["HASIL", "JUMLAH PERBELANJAAN"])
        ].copy()

        df_chart_pl = df_chart_pl.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_chart_pl["NILAI"] = pd.to_numeric(df_chart_pl["NILAI"], errors="coerce").fillna(0)
        df_chart_pl["NILAI_JUTA"] = df_chart_pl["NILAI"] / 1_000_000
        df_chart_pl["LABEL"] = df_chart_pl["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        y_max = df_chart_pl["NILAI_JUTA"].max()

        fig_pl = px.bar(
            df_chart_pl,
            x="JENIS",
            y="NILAI_JUTA",
            color="PERKARA",
            barmode="group",
            text="LABEL",
            height=720,
            color_discrete_map={
                "HASIL": "#d8b4d8",
                "JUMLAH PERBELANJAAN": "#e8742f"
            },
            labels={
                "JENIS": "",
                "NILAI_JUTA": "Juta",
                "PERKARA": ""
            },
            title="PRESTASI HASIL & PERBELANJAAN CIDB SEHINGGA SUKU KEDUA 2026"
        )

        fig_pl.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=14, color="black", family="Arial")
        )

        fig_pl.update_layout(
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=160, b=150, l=90, r=90),
            xaxis_title="",
            yaxis_title="Juta",
            xaxis_tickangle=0,
            yaxis_range=[0, y_max * 1.25 if y_max else 1],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        st.plotly_chart(fig_pl, use_container_width=True)




        df_data_pilihan = df_pl_jadual6.copy()
        sheet_name = "JADUAL6_PL"

    elif pilihan_pl == "Pecahan Belanja CIDB":

        df_belanja_chart = df_pecahan_belanja.melt(
            id_vars="KATEGORI",
            value_vars=["BAJET 2026", "BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_belanja_chart["NILAI"] = pd.to_numeric(df_belanja_chart["NILAI"], errors="coerce").fillna(0)
        df_belanja_chart["NILAI_JUTA"] = df_belanja_chart["NILAI"] / 1_000_000
        df_belanja_chart["LABEL"] = df_belanja_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        y_max = df_belanja_chart["NILAI_JUTA"].max()

        fig_belanja = px.bar(
            df_belanja_chart,
            x="KATEGORI",
            y="NILAI_JUTA",
            color="JENIS",
            barmode="group",
            text="LABEL",
            height=720,
            color_discrete_sequence=["#d8b4d8", "#e8742f", "#8fd17f", "#7aa6c2"],
            labels={
                "KATEGORI": "",
                "NILAI_JUTA": "Juta",
                "JENIS": ""
            },
            title="PECAHAN BELANJA CIDB SEHINGGA SUKU KEDUA 2026"
        )

        fig_belanja.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=13, color="black", family="Arial")
        )

        fig_belanja.update_layout(
            template="plotly_white",
            margin=dict(t=160, b=150, l=90, r=90),
            xaxis_tickangle=0,
            yaxis_title="Juta",
            yaxis_range=[0, y_max * 1.30 if y_max else 1],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        st.plotly_chart(fig_belanja, use_container_width=True)

        df_belanja_pct = df_pecahan_belanja.melt(
            id_vars="KATEGORI",
            value_vars=["Prestasi Bajet 06-2026", "Prestasi Bajet 2026", "Prestasi 06-26 vs 06-25"],
            var_name="JENIS",
            value_name="PERATUS"
        )




        df_data_pilihan = df_pecahan_belanja.copy()
        sheet_name = "PECAHAN_BELANJA"

    else:

        # =========================================================
        # CARTA TAMBAHAN:
        # SURPLUS/(DEFISIT) PRESTASI BAJET CIDB
        # TERMASUK SUSUT NILAI DAN HUTANG RAGU
        #
        # Formula:
        # Termasuk S/Nilai & H.Ragu = Hasil - Jumlah Perbelanjaan
        # Nota:
        # BAJET 2026 = 485j - 485j = 0
        # =========================================================
        hasil_term = df_pl_jadual6[
            df_pl_jadual6["PERKARA"].astype(str).str.strip().str.lower().eq("hasil")
        ].iloc[0]

        jumlah_perbelanjaan_term = df_pl_jadual6[
            df_pl_jadual6["PERKARA"].astype(str).str.strip().eq("Jumlah Perbelanjaan")
        ].iloc[0]

        df_surplus_termasuk_chart = pd.DataFrame({
            "JENIS": [
                "BAJET 2026",
                "BAJET 06-2026",
                "SEBENAR 06-2026",
                "SEBENAR 06-2025"
            ],
            "NILAI": [
                hasil_term["BAJET 2026"] - jumlah_perbelanjaan_term["BAJET 2026"],
                hasil_term["BAJET 06-2026"] - jumlah_perbelanjaan_term["BAJET 06-2026"],
                hasil_term["SEBENAR 06-2026"] - jumlah_perbelanjaan_term["SEBENAR 06-2026"],
                hasil_term["SEBENAR 06-2025"] - jumlah_perbelanjaan_term["SEBENAR 06-2025"],
            ]
        })

        df_surplus_termasuk_chart["NILAI"] = pd.to_numeric(
            df_surplus_termasuk_chart["NILAI"],
            errors="coerce"
        ).fillna(0)

        df_surplus_termasuk_chart["NILAI_JUTA"] = (
            df_surplus_termasuk_chart["NILAI"] / 1_000_000
        )

        df_surplus_termasuk_chart["LABEL"] = (
            df_surplus_termasuk_chart["NILAI_JUTA"]
            .map(lambda x: f"{x:,.2f}")
        )

        fig_surplus_termasuk = px.bar(
            df_surplus_termasuk_chart,
            x="JENIS",
            y="NILAI_JUTA",
            text="LABEL",
            height=720,
            color="JENIS",
            color_discrete_map={
                "BAJET 2026": "#d9534f",
                "BAJET 06-2026": "#F59E0B",
                "SEBENAR 06-2026": "#2e8b57",
                "SEBENAR 06-2025": "#9CA3AF"
            },
            labels={
                "JENIS": "",
                "NILAI_JUTA": "Juta"
            },
            title=(
                "SURPLUS/(DEFISIT) PRESTASI BAJET CIDB "
                "TERMASUK SUSUT NILAI & HUTANG RAGU"
            )
        )

        fig_surplus_termasuk.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(
                size=14,
                color="black",
                family="Arial"
            )
        )

        min_y_termasuk = df_surplus_termasuk_chart["NILAI_JUTA"].min()
        max_y_termasuk = df_surplus_termasuk_chart["NILAI_JUTA"].max()

        fig_surplus_termasuk.update_layout(
            template="plotly_white",
            showlegend=False,
            margin=dict(t=170, b=150, l=90, r=90),
            xaxis_tickangle=0,
            yaxis_title="Juta",
            yaxis_range=[
                min_y_termasuk * 1.35 if min_y_termasuk < 0 else 0,
                max_y_termasuk * 1.30 if max_y_termasuk > 0 else 1
            ],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        # DOTTED untuk SEBENAR 06-2025
        fig_surplus_termasuk.update_traces(
            marker_pattern_shape=".",
            marker_pattern_fgcolor="white",
            marker_pattern_size=7,
            marker_pattern_solidity=0.25,
            selector=dict(name="SEBENAR 06-2025")
        )

        st.plotly_chart(
            fig_surplus_termasuk,
            use_container_width=True
        )


        df_surplus = df_pl[
            df_pl["PERKARA"].str.contains("LEBIHAN", na=False)
        ].copy()

        df_surplus_chart = df_surplus.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )

        df_surplus_chart["NILAI"] = pd.to_numeric(df_surplus_chart["NILAI"], errors="coerce").fillna(0)
        df_surplus_chart["NILAI_JUTA"] = df_surplus_chart["NILAI"] / 1_000_000
        df_surplus_chart["LABEL"] = df_surplus_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")

        fig_surplus = px.bar(
            df_surplus_chart,
            x="JENIS",
            y="NILAI_JUTA",
            text="LABEL",
            height=720,
            color="JENIS",
            color_discrete_map={
                "BAJET 2026": "#d9534f",
                "BAJET 06-2026": "#F59E0B",
                "SEBENAR 06-2026": "#2e8b57",
                "SEBENAR 06-2025": "#9CA3AF"
            },
            labels={
                "JENIS": "",
                "NILAI_JUTA": "Juta"
            },
            title="LEBIHAN/(KURANGAN) PENDAPATAN TIDAK TERMASUK S/NILAI & H.RAGU"
        )

        fig_surplus.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            constraintext="none",
            textfont=dict(size=14, color="black", family="Arial")
        )

        min_y = df_surplus_chart["NILAI_JUTA"].min()
        max_y = df_surplus_chart["NILAI_JUTA"].max()

        fig_surplus.update_layout(
            template="plotly_white",
            showlegend=False,
            margin=dict(t=170, b=150, l=90, r=90),
            xaxis_tickangle=0,
            yaxis_title="Juta",
            yaxis_range=[
                min_y * 1.35 if min_y < 0 else 0,
                max_y * 1.30 if max_y > 0 else 1
            ],
            uniformtext_minsize=7,
            uniformtext_mode="show"
        )

        # DOTTED untuk SEBENAR 06-2025
        fig_surplus.update_traces(
            marker_pattern_shape=".",
            marker_pattern_fgcolor="white",
            marker_pattern_size=7,
            marker_pattern_solidity=0.25,
            selector=dict(name="SEBENAR 06-2025")
        )

        st.plotly_chart(fig_surplus, use_container_width=True)




        df_untung = df_pl_jadual6[
            df_pl_jadual6["PERKARA"].isin([
                "Untung sebelum cukai dan zakat",
                "Untung selepas cukai dan zakat",
                "Lebihan/(Kurangan) Pendapatan Termasuk S/Nilai & H.Ragu",
                "(-) S/Nilai & H. Ragu",
                "Lebihan/(Kurangan) Pendapatan Tidak Termasuk S/Nilai & H.Ragu"
            ])
        ].copy()

        df_untung_chart = df_untung.melt(
            id_vars="PERKARA",
            value_vars=["BAJET 2026", "BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"],
            var_name="JENIS",
            value_name="NILAI"
        )
        df_untung_chart["NILAI_JUTA"] = pd.to_numeric(df_untung_chart["NILAI"], errors="coerce").fillna(0) / 1_000_000
        df_untung_chart["LABEL"] = df_untung_chart["NILAI_JUTA"].map(lambda x: f"{x:,.2f}")




        df_data_pilihan = df_pl_jadual6.copy()
        sheet_name = "SURPLUS_DEFISIT"

    st.markdown("### 📋 Data P&L - Jadual 6")

    df_show = df_data_pilihan.copy()

    money_cols = [
        "BAJET 2026", "BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"
    ]
    percent_cols = [
        "Prestasi Bajet 06-2026", "Prestasi Bajet 2026", "Prestasi 06-26 vs 06-25"
    ]

    for col in money_cols:
        if col in df_show.columns:
            df_show[col] = pd.to_numeric(df_show[col], errors="coerce").fillna(0).apply(format_comma)

    for col in percent_cols:
        if col in df_show.columns:
            df_show[col] = pd.to_numeric(df_show[col], errors="coerce").map(
                lambda x: "-" if pd.isna(x) else f"{x:.0f}%"
            )

    # Papar '-' untuk Cukai/Zakat yang tiada nilai sasaran/sebenar dalam jadual asal.
    if "PERKARA" in df_show.columns:
        cukai_zakat_mask = df_show["PERKARA"].astype(str).isin(["Cukai", "Zakat"])
        for col in ["BAJET 06-2026", "SEBENAR 06-2026", "SEBENAR 06-2025"]:
            if col in df_show.columns:
                df_show.loc[cukai_zakat_mask, col] = "-"
        for col in percent_cols:
            if col in df_show.columns:
                df_show.loc[cukai_zakat_mask, col] = "-"

    st.dataframe(df_show, use_container_width=True, hide_index=True)

    excel_pl = to_excel(df_data_pilihan, sheet_name=sheet_name)

    st.download_button(
        "📥 Download Data P&L Excel",
        data=excel_pl,
        file_name="Data_PL_Jadual6_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

elif menu == "4. Balance Sheet":

    # =======================
    # BALANCE SHEET
    # Rujukan Word:
    # Jadual 7: Penyata Kedudukan Kewangan pada Suku Kedua 2026
    #
    # Data sebenar daripada Word:
    # 06-2026 dan 2025
    # =======================

    st.markdown("### 📊 PENYATA KEDUDUKAN KEWANGAN CIDB PADA 06-2026")

    df_bs = pd.DataFrame({
        "PERKARA": [
            "ASET 2025",
            "LIABILITI & A.BERSIH 2025",
            "ASET 06-2026",
            "LIABILITI & A.BERSIH 06-2026"
        ],
        "ASET BERSIH (RM)": [0, 1_140_889_719, 0, 1_277_981_314],
        "BUKAN SEMASA (RM)": [493_358_471, 35_235_965, 491_662_480, 34_936_675],
        "SEMASA (RM)": [742_014_399, 59_247_186, 833_461_314, 12_205_805],
        "JUMLAH": [1_235_372_870, 1_235_372_870, 1_325_123_794, 1_325_123_794]
    })

    # =======================
    # CARTA BALANCE SHEET
    # =======================
    df_bs_chart = df_bs.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_chart[col] = pd.to_numeric(
            df_bs_chart[col],
            errors="coerce"
        ).fillna(0)

    df_bs_chart_juta = df_bs_chart.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_chart_juta[col] = df_bs_chart_juta[col] / 1_000_000

    fig_bs = go.Figure()

    warna_bs = {
        "ASET BERSIH (RM)": "#b7e4a8",
        "BUKAN SEMASA (RM)": "#ef7130",
        "SEMASA (RM)": "#7ec8e3"
    }

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)"]:
        fig_bs.add_trace(
            go.Bar(
                x=df_bs_chart_juta["PERKARA"],
                y=df_bs_chart_juta[col],
                name=col,
                marker_color=warna_bs[col],
                text=[
                    "-" if nilai == 0 else f"{nilai:,.2f}"
                    for nilai in df_bs_chart_juta[col]
                ],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(
                    size=13,
                    color="#2c3e50",
                    family="Arial"
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    + col
                    + ": RM %{customdata:,.2f}<extra></extra>"
                ),
                customdata=df_bs_chart[col]
            )
        )

    # Label jumlah di atas setiap stacked bar
    fig_bs.add_trace(
        go.Scatter(
            x=df_bs_chart_juta["PERKARA"],
            y=df_bs_chart_juta["JUMLAH"],
            mode="text",
            text=[
                f"{nilai:,.2f}"
                for nilai in df_bs_chart_juta["JUMLAH"]
            ],
            textposition="top center",
            textfont=dict(
                size=16,
                color="black",
                family="Arial"
            ),
            name="Jumlah",
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig_bs.update_layout(
        title="PENYATA KEDUDUKAN KEWANGAN CIDB PADA 06-2026",
        barmode="stack",
        height=720,
        template="plotly_white",
        margin=dict(t=100, b=140, l=80, r=60),
        xaxis=dict(
            title="",
            tickangle=0,
            automargin=True
        ),
        yaxis=dict(
            title="Juta",
            rangemode="tozero"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5
        ),
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    st.plotly_chart(
        fig_bs,
        use_container_width=True
    )

    # =======================
    # DATA BALANCE SHEET
    # =======================
    st.markdown("### 📋 Data Balance Sheet")

    df_bs_show = df_bs.copy()

    for col in ["ASET BERSIH (RM)", "BUKAN SEMASA (RM)", "SEMASA (RM)", "JUMLAH"]:
        df_bs_show[col] = (
            pd.to_numeric(df_bs_show[col], errors="coerce")
            .fillna(0)
            .apply(format_comma)
        )

    df_bs_show.loc[
        df_bs["ASET BERSIH (RM)"] == 0,
        "ASET BERSIH (RM)"
    ] = "-"

    st.dataframe(
        df_bs_show,
        use_container_width=True,
        hide_index=True
    )

    excel_bs = to_excel(
        df_bs,
        sheet_name="BALANCE_SHEET"
    )

    st.download_button(
        "📥 Download Balance Sheet Excel",
        data=excel_bs,
        file_name="Balance_Sheet_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

elif menu == "5. Cash Flow":

    # =======================
    # CASH FLOW
    # Rujukan Word:
    # Jadual 8: Penyata Aliran Tunai bagi tahun kewangan berakhir Suku Kedua 2026
    #
    # Data diekstrak daripada Word:
    # 06-2026 dan 2025
    # =======================

    st.markdown("### 📊 PENYATA ALIRAN TUNAI CIDB 06-2026")

    df_cf = pd.DataFrame({
        "PERKARA": ["SEBENAR 2025", "SEBENAR 06-2026"],
        "BAKI TUNAI AWAL (RM)": [608_091_383, 693_799_652],
        "AKT. OPERASI (RM)": [108_433_429, 66_291_475],
        "AKT. PELABURAN (RM)": [-22_725_160, 2_613_349],
        "AKT. PEMBIAYAAN (RM)": [0, 0],
        "PENGURANGAN/PENAMBAHAN BERSIH (RM)": [85_708_269, 68_904_824],
        "BAKI TUNAI AKHIR (RM)": [693_799_652, 762_704_476]
    })

    # =======================
    # CARTA CASH FLOW
    # Ikut gaya contoh: horizontal bar untuk
    # Baki Tunai Awal, Aktiviti Operasi, Aktiviti Pelaburan, Baki Tunai Akhir.
    # =======================
    df_cf_chart = df_cf.copy()

    chart_cols = [
        "BAKI TUNAI AKHIR (RM)",
        "AKT. PELABURAN (RM)",
        "AKT. OPERASI (RM)",
        "BAKI TUNAI AWAL (RM)"
    ]

    for col in chart_cols:
        df_cf_chart[col] = (
            pd.to_numeric(df_cf_chart[col], errors="coerce")
            .fillna(0)
            / 1_000_000
        )

    fig_cf = go.Figure()

    warna_cf = {
        "BAKI TUNAI AKHIR (RM)": "#3b821f",
        "AKT. PELABURAN (RM)": "#20dbe0",
        "AKT. OPERASI (RM)": "#ffc000",
        "BAKI TUNAI AWAL (RM)": "#00f29a"
    }

    for col in chart_cols:
        fig_cf.add_trace(
            go.Bar(
                y=df_cf_chart["PERKARA"],
                x=df_cf_chart[col],
                name=col,
                orientation="h",
                marker_color=warna_cf[col],
                text=[
                    f"{x:,.2f}"
                    for x in df_cf_chart[col]
                ],
                textposition="outside",
                textfont=dict(
                    size=14,
                    color="#3b3b3b",
                    family="Arial"
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    + col
                    + ": RM %{customdata:,.2f}<extra></extra>"
                ),
                customdata=df_cf[col]
            )
        )

    fig_cf.update_layout(
        title="PENYATA ALIRAN TUNAI CIDB 06-2026",
        template="plotly_white",
        barmode="group",
        height=720,
        margin=dict(
            t=100,
            b=130,
            l=140,
            r=80
        ),
        xaxis=dict(
            title="Juta",
            zeroline=True,
            tickformat=","
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[
                "SEBENAR 2025",
                "SEBENAR 06-2026"
            ]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    st.plotly_chart(
        fig_cf,
        use_container_width=True
    )

    # =======================
    # DATA CASH FLOW
    # =======================
    st.markdown("### 📋 Data Cash Flow")

    df_cf_show = df_cf.copy()

    for col in [
        "BAKI TUNAI AWAL (RM)",
        "AKT. OPERASI (RM)",
        "AKT. PELABURAN (RM)",
        "AKT. PEMBIAYAAN (RM)",
        "PENGURANGAN/PENAMBAHAN BERSIH (RM)",
        "BAKI TUNAI AKHIR (RM)"
    ]:
        df_cf_show[col] = (
            pd.to_numeric(df_cf_show[col], errors="coerce")
            .fillna(0)
            .apply(format_comma)
        )

    st.dataframe(
        df_cf_show,
        use_container_width=True,
        hide_index=True
    )

    excel_cf = to_excel(
        df_cf,
        sheet_name="CASH_FLOW"
    )

    st.download_button(
        "📥 Download Cash Flow Excel",
        data=excel_cf,
        file_name="Cash_Flow_CIDB.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =========================================================
