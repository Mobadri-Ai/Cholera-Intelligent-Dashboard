import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Cholera Monitoring Dashboard", layout="wide")

# تحميل البيانات
@st.cache_data
def load_data():
    data = pd.read_csv("data.csv", parse_dates=["date"])
    return data

data = load_data()

# الواجهة العلوية
st.markdown("<h1 style='text-align:center; color:#007BFF;'>🌍 Cholera Monitoring Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Real-time outbreak visualization and analytics</p>", unsafe_allow_html=True)
st.markdown("---")

# إحصائيات عامة
total_cases = data["cases"].sum()
total_deaths = data["deaths"].sum()
death_rate = (total_deaths / total_cases) * 100 if total_cases > 0 else 0
last_update = data["date"].max().strftime("%Y-%m-%d")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🦠 Total Cases", f"{total_cases}")
col2.metric("☠️ Total Deaths", f"{total_deaths}")
col3.metric("📉 Death Rate", f"{death_rate:.2f}%")
col4.metric("📅 Last Update", last_update)

st.markdown("---")

# الشريط الجانبي
st.sidebar.header("Filter Options")
regions = ["All"] + sorted(data["location"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region:", regions)
filtered_data = data[data["location"] == selected_region] if selected_region != "All" else data

# إنشاء الخريطة
m = folium.Map(location=[11.5, 30.0], zoom_start=6, tiles="CartoDB positron")
for _, row in filtered_data.iterrows():
    color = "red" if row["deaths"] > 0 else "blue"
    popup = f"<b>{row['location']}</b><br>Date: {row['date'].strftime('%Y-%m-%d')}<br>Cases: {row['cases']}<br>Deaths: {row['deaths']}"
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5 + row["cases"] * 0.3,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=popup
    ).add_to(m)

# عرض الخريطة
st.subheader("🗺️ Cholera Outbreak Map")
st_folium(m, width=1100, height=550)

# رسم بياني
st.subheader("📈 Daily Cases Over Time")
fig = px.line(filtered_data, x="date", y="cases", color="location",
              title="Cases Trend by Location",
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# جدول البيانات
st.subheader("📋 Data Table")
st.dataframe(filtered_data)
