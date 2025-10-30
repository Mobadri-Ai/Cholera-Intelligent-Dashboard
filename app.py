import streamlit as st
from streamlit_folium import st_folium
import folium

# ----- Page Config -----
st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide")

# ----- Dark Mode Toggle -----
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ----- CSS -----
dark_bg = "#0e1117"
light_bg = "#f4f6fa"

st.markdown(f"""
<style>
body {{
    background-color: {'#0e1117' if st.session_state.dark_mode else '#f4f6fa'};
}}
.app-container {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    margin-top: 10px;
}}
.map-container {{
    height: 350px !important;
}}
@media (max-width: 768px) {{
    .map-container {{
        height: 250px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ----- Header -----
st.markdown(
    "<h2 style='text-align:center; font-weight:700;'>Disease Monitoring Dashboard</h2>",
    unsafe_allow_html=True
)

st.button("🌙 Toggle Dark Mode", on_click=toggle_dark)

# ----- Main Card -----
st.markdown("<div class='app-container'>", unsafe_allow_html=True)

st.write("### 🗺️ Real-Time Disease Spread Map")

# ----- Map -----
m = folium.Map(location=[15.5007, 32.5599], zoom_start=6)
folium.Marker([15.5, 32.55], popup="Sample Location").add_to(m)

st_map = st_folium(m, width="100%", height=350)

# ----- Power BI Section -----
st.write("### 📊 Analytics Dashboard (Power BI)")
st.markdown("""
<iframe title="PowerBI Dashboard"
width="100%" height="500"
src="YOUR_POWER_BI_IFRAME_LINK"
frameborder="0" allowFullScreen="true"></iframe>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
