import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ======================
# إعداد الصفحة العامة
# ======================
st.set_page_config(
    page_title="Cholera Monitoring Dashboard",
    layout="wide",
    page_icon="🌍",
)

# ======================
# تحميل البيانات
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

data = load_data()

# ======================
# إعدادات الوضع (داكن / فاتح)
# ======================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

theme = st.session_state.theme

# ======================
# شريط علوي احترافي
# ======================
st.markdown(f"""
    <style>
        body {{
            background-color: {"#f7faff" if theme == "light" else "#121212"};
            color: {"#212529" if theme == "light" else "#f1f1f1"};
            font-family: 'Segoe UI', sans-serif;
        }}
        .navbar {{
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 60px;
            background-color: {"#0d6efd" if theme == "light" else "#1e1e1e"};
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 25px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        .navbar h1 {{
            color: white;
            font-size: 20px;
            margin: 0;
        }}
        .navbar button {{
            background-color: {"#ffffff" if theme == "light" else "#2b2b2b"};
            color: {"#0d6efd" if theme == "light" else "#f8f9fa"};
            border: none;
            border-radius: 8px;
            padding: 5px 14px;
            cursor: pointer;
            font-size: 14px;
        }}
        .main-content {{
            margin-top: 80px;
            padding: 15px 25px;
        }}
        iframe {{
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <div class="navbar">
        <h1>🌍 Cholera Monitoring Dashboard</h1>
        <form action="" method="get">
            <button onclick="window.location.reload()">{"🌙 Dark Mode" if theme == "light" else "☀️ Light Mode"}</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# ======================
# محتوى الصفحة
# ======================
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown(f"""
        <h3 style="color:{'#0d6efd' if theme == 'light' else '#9cd1ff'};">
        🗺️ Cholera Outbreak Map</h3>
    """, unsafe_allow_html=True)

    # إنشاء الخريطة
    m = folium.Map(
        location=[11.5, 30.0],
        zoom_start=6,
        tiles="CartoDB dark_matter" if theme == "dark" else "CartoDB positron"
    )

    for _, row in data.iterrows():
        popup_text = f"<b>{row['location']}</b><br>Cases: {row['cases']}<br>Deaths: {row['deaths']}"
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6 + row["cases"] * 0.3,
            color="red" if row["deaths"] > 0 else "#0d6efd",
            fill=True,
            fill_color="orange" if row["deaths"] > 0 else "#66b2ff",
            popup=popup_text,
        ).add_to(m)

    st_folium(m, width=750, height=380)

    # جدول البيانات
    st.markdown(f"""
        <h3 style="color:{'#0d6efd' if theme == 'light' else '#9cd1ff'};">📋 Reported Cases Data</h3>
    """, unsafe_allow_html=True)
    st.dataframe(data, use_container_width=True)

    # لوحة Power BI
    st.markdown(f"""
        <h3 style="color:{'#0d6efd' if theme == 'light' else '#9cd1ff'};">📊 Power BI Analytics</h3>
    """, unsafe_allow_html=True)

    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzA2Y2UxZ..."  # استبدل هذا برابط لوحتك
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <iframe title="Power BI Dashboard" width="100%" height="550"
            src="{power_bi_url}"
            frameborder="0" allowFullScreen="true"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

    # التذييل
    st.markdown(f"""
        <hr style='margin-top: 40px;'>
        <p style='text-align:center; color:{"#6c757d" if theme == "light" else "#aaaaaa"}; font-size:13px;'>
        © 2025 Mohamed Badri – Cholera Monitoring System | Designed with ❤️ using Streamlit
        </p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
