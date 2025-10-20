import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ======================
# إعدادات الصفحة العامة
# ======================
st.set_page_config(
    page_title="Cholera Monitoring Dashboard",
    layout="centered",
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
# تنسيق العنوان والرأس
# ======================
st.markdown("""
    <style>
        body {background-color: #f7faff;}
        .title {
            text-align: center;
            color: #0d6efd;
            font-size: 32px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #495057;
            font-size: 16px;
            margin-bottom: 30px;
        }
        .section-header {
            font-size: 20px;
            color: #0d6efd;
            margin-top: 40px;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 8px;
        }
        iframe {
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🌍 Cholera Monitoring & Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Early warning system powered by Streamlit + Power BI + Folium</p>", unsafe_allow_html=True)

# ======================
# خريطة تفاعلية (صغيرة ومناسبة للجوال)
# ======================
st.markdown("<h3 class='section-header'>🗺️ Cholera Outbreak Map</h3>", unsafe_allow_html=True)

m = folium.Map(location=[11.5, 30.0], zoom_start=6, tiles="CartoDB positron")

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

# عرض الخريطة بحجم متوافق مع الجوال
st_folium(m, width=700, height=380)

# ======================
# جدول البيانات
# ======================
st.markdown("<h3 class='section-header'>📋 Reported Cases Data</h3>", unsafe_allow_html=True)
st.dataframe(data, use_container_width=True)

# ======================
# لوحة Power BI أسفل الصفحة
# ======================
st.markdown("<h3 class='section-header'>📊 Advanced Analytics (Power BI)</h3>", unsafe_allow_html=True)

power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzA2Y2UxZ..."  # 🔗 استبدله برابط لوحتك

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

# ======================
# تذييل أنيق
# ======================
st.markdown("""
    <hr style='margin-top: 40px;'>
    <p style='text-align:center; color:#6c757d; font-size:13px;'>
    © 2025 Mohamed Badri – Cholera Monitoring System | Designed with ❤️ using Streamlit
    </p>
""", unsafe_allow_html=True)
