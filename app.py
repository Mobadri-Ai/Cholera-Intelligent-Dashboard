import streamlit as st
from streamlit_folium import st_folium
import folium

# ========== Settings ==========
st.set_page_config(page_title="Cholera Dashboard", layout="wide")

# ========== Dark Mode ==========
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

dark_bg = "#0e1117"
light_bg = "#f8f9fc"

# ========== Style ==========
st.markdown(f"""
<style>
body {{
    background-color: {'#0e1117' if st.session_state.dark_mode else '#f8f9fc'} !important;
}}

.navbar {{
    padding: 15px;
    display: flex;
    justify-content: space-between;
    background: {'#111827' if st.session_state.dark_mode else '#ffffff'};
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}

.title {{
    font-size: 20px;
    font-weight: 700;
    color: {'#ffffff' if st.session_state.dark_mode else '#000000'};
}}

.map-container {{
    height: 330px;
    border-radius: 12px;
    overflow: hidden;
}}

@media (max-width: 768px) {{
    .map-container {{
        height: 230px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ========== Navbar ==========
st.markdown("""
<div class='navbar'>
    <div class='title'>🌍 Cholera Monitoring Dashboard</div>
</div>
""", unsafe_allow_html=True)

st.button("🌙 Toggle Dark Mode", on_click=toggle_dark_mode)

# ========== MAP ==========
st.subheader("🗺️ Real-Time Disease Map")

map_center = [15.50, 32.55]
m = folium.Map(location=map_center, zoom_start=6)
folium.Marker(map_center, popup="Sample Case").add_to(m)

st_folium(m, width="100%", height=330, returned_objects=[])

# ========== Power BI ==========
st.subheader("📊 Analytics Dashboard (Power BI)")

st.markdown("""
<iframe title="pbi" width="100%" height="550"
src="YOUR_POWER_BI_IFRAME_LINK"
frameborder="0" allowFullScreen="true"></iframe>
""", unsafe_allow_html=True)
