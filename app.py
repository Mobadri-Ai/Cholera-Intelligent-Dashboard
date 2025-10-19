import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# إعداد الصفحة
st.set_page_config(page_title="Cholera Monitoring Dashboard", layout="wide")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

data = load_data()

# عنوان الصفحة
st.markdown("<h1 style='text-align:center; color:#007BFF;'>🌍 Cholera Monitoring & Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Powered by Streamlit + Power BI + Folium</p>", unsafe_allow_html=True)
st.markdown("---")

# إنشاء التبويبات
tab1, tab2 = st.tabs(["🗺️ Cholera Map", "📊 Power BI Analytics"])

# ==== التبويب الأول: الخريطة ====
with tab1:
    st.subheader("🗺️ Cholera Outbreak Map")

    # إنشاء خريطة Folium
    m = folium.Map(location=[11.5, 30.0], zoom_start=6, tiles="CartoDB positron")

    for _, row in data.iterrows():
        popup_text = f"<b>{row['location']}</b><br>Cases: {row['cases']}<br>Deaths: {row['deaths']}"
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6 + row["cases"] * 0.3,
            color="red" if row["deaths"] > 0 else "blue",
            fill=True,
            fill_color="orange" if row["deaths"] > 0 else "lightblue",
            popup=popup_text
        ).add_to(m)

    st_folium(m, width=1100, height=550)
    st.markdown("### 📋 Data Table")
    st.dataframe(data)

# ==== التبويب الثاني: لوحة Power BI ====
with tab2:
    st.subheader("📊 Interactive Analytics from Power BI")

    st.markdown("""
        <p>Below is an embedded Power BI dashboard that visualizes cholera cases, death rates, and trends.
        The dashboard is connected to live data and updates automatically.</p>
    """, unsafe_allow_html=True)

    # 🔗 رابط لوحة Power BI الخاصة بك (استبدله برابطك)
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzA2Y2UxZ..."  # ضع هنا رابطك الفعلي

    st.markdown(
        f'<iframe width="100%" height="600" src="{power_bi_url}" frameborder="0" allowFullScreen="true"></iframe>',
        unsafe_allow_html=True
    )
