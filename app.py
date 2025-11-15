import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta

# --- 1. الإعدادات والبيانات الوهمية (Mock Data & Setup) ---

# تعيين إعدادات الصفحة
st.set_page_config(
    page_title="CHOLERA Intelligent Dashboard (CID)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- محاكاة قاعدة بيانات Supabase (باستخدام Session State) ---
def initialize_data():
    """تهيئة البيانات الأولية للحالات والخريطة."""
    if 'cholera_cases' not in st.session_state:
        # بيانات وهمية لأغراض العرض (خطوط الطول والعرض لمدينة وهمية في إفريقيا)
        case_data = {
            'Date': [datetime.now() - timedelta(days=i) for i in range(30)],
            'Confirmed_Cases': [random.randint(5, 30) for _ in range(30)],
            'Deaths': [random.randint(0, 2) for _ in range(30)],
            'Lat': [12.65 + (random.random() - 0.5) * 0.5 for _ in range(30)],
            'Lon': [15.05 + (random.random() - 0.5) * 0.5 for _ in range(30)],
            'Type': random.choices(['Confirmed Case', 'Suspected Case', 'Positive Water Sample'], k=30),
            'Severity': [random.choice(['Low', 'Medium', 'High']) for _ in range(30)]
        }
        st.session_state.cholera_cases = pd.DataFrame(case_data).sort_values('Date').reset_index(drop=True)
        st.session_state.cholera_cases['Date'] = st.session_state.cholera_cases['Date'].dt.date

    if 'sites_data' not in st.session_state:
        # بيانات وهمية لمواقع التدخل
        st.session_state.sites_data = {
            'Chlorine_Distribution': [
                {'Lat': 12.8, 'Lon': 15.1, 'Status': 'Active'},
                {'Lat': 12.3, 'Lon': 15.4, 'Status': 'Inactive'}
            ],
            'IDP_Camps': [
                {'Lat': 12.7, 'Lon': 14.9, 'Population': 5000},
                {'Lat': 12.5, 'Lon': 15.3, 'Population': 12000}
            ]
        }

    if 'language' not in st.session_state:
        st.session_state.language = 'ar'
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True

initialize_data()

# --- 2. الترجمة (Localization) واللغة ---
T = {
    'ar': {
        'title': 'لوحة التحكم الذكية للكوليرا (CID)',
        'subtitle': 'نظام الإنذار المبكر والتحليل المتقدم للأوبئة',
        'dashboard_tab': 'لوحة التحكم الرئيسية',
        'ews_tab': 'الإنذار المبكر والتحليل الذكي',
        'reporting_tab': 'الإبلاغ والشكاوى',
        'lang_switch': 'اللغة (Language)',
        'mode_switch': 'الوضع الليلي',
        'mode_switch_light': 'الوضع النهاري',
        'risk_level': 'مستوى الإنذار الحالي',
        'region_select': 'اختيار المنطقة الإدارية',
        'cases_chart_title': 'تطور الحالات المؤكدة اليومية (آخر 30 يومًا)',
        'total_cases': 'إجمالي الحالات المؤكدة',
        'total_deaths': 'إجمالي الوفيات',
        'pos_water_samples': 'عينات المياه الإيجابية',
        'map_title': 'خريطة تفاعلية للمخاطر والموارد',
        'map_tooltip_case': 'حالة مؤكدة',
        'map_tooltip_water': 'عينة مياه إيجابية',
        'map_tooltip_chlorine': 'موقع توزيع الكلور',
        'map_tooltip_idp': 'مخيّم نازحين (S)' ,
        'prediction_title': 'تنبؤ المخاطر (AI)',
        'prediction_7d': 'مناطق معرضة للخطر (7 أيام)',
        'prediction_30d': 'مناطق معرضة للخطر (30 يومًا)',
        'analysis_title': 'تحليل النصوص والتقارير',
        'recurring_issues': 'المشكلات المتكررة (من تقارير المنظمات ووسائل التواصل)',
        'add_case_title': 'إضافة حالة أو موقع جديد (محاكاة لإدخال البيانات)',
        'case_location': 'الموقع الإداري للحالة',
        'case_lat': 'خط العرض (Latitude)',
        'case_lon': 'خط الطول (Longitude)',
        'case_type': 'نوع الإدخال',
        'submit_case': 'إرسال الإدخال',
        'complaint_title': 'صندوق الشكاوى والملاحظات',
        'complaint_type': 'نوع الشكوى/البلاغ',
        'complaint_details': 'تفاصيل الشكوى (نقص كلور، حالة جديدة، إلخ.)',
        'submit_complaint': 'إرسال الشكوى عبر محاكاة الواتساب',
        'success_case': 'تمت إضافة الحالة/الموقع بنجاح.',
        'success_complaint': 'تم استلام الشكوى بنجاح. سيتم إرسال تنبيه للسلطات المعنية.',
        'risk_high': 'خطر عالي (تجاوز مؤشرات الوباء)',
        'risk_medium': 'خطر متوسط (مراقبة مشددة)',
        'risk_low': 'خطر منخفض (استقرار)',
        'alert_box_high': '🚨 تنبيه عاجل: تم تجاوز مؤشر الخطر في مناطق (أ، ب، ج). يوصى بتكثيف الاستجابة الفورية.',
        'alert_box_medium': '⚠️ تحذير: ارتفاع طفيف في الحالات بمنطقة (د). يوصى بزيادة مراقبة جودة المياه.',
        'alert_box_low': '✅ الوضع مستقر: لا توجد مؤشرات خطر حرجة حالياً.',
        'pbi_title': 'لوحة Power BI: تحليل شامل ومتقدم',
    },
    'en': {
        'title': 'CHOLERA Intelligent Dashboard (CID)',
        'subtitle': 'Early Warning System and Advanced Epidemic Analysis',
        'dashboard_tab': 'Main Dashboard',
        'ews_tab': 'Early Warning & Smart Analysis',
        'reporting_tab': 'Reporting & Complaints',
        'lang_switch': 'اللغة (Language)',
        'mode_switch': 'Dark Mode',
        'mode_switch_light': 'Light Mode',
        'risk_level': 'Current Alert Level',
        'region_select': 'Select Administrative Region',
        'cases_chart_title': 'Daily Confirmed Cases Trend (Last 30 Days)',
        'total_cases': 'Total Confirmed Cases',
        'total_deaths': 'Total Deaths',
        'pos_water_samples': 'Positive Water Samples',
        'map_title': 'Interactive Map of Risks and Resources',
        'map_tooltip_case': 'Confirmed Case',
        'map_tooltip_water': 'Positive Water Sample',
        'map_tooltip_chlorine': 'Chlorine Distribution Site',
        'map_tooltip_idp': 'IDP Camp',
        'prediction_title': 'Risk Prediction (AI)',
        'prediction_7d': 'High-Risk Zones (7 Days)',
        'prediction_30d': 'High-Risk Zones (30 Days)',
        'analysis_title': 'Text and Report Analysis',
        'recurring_issues': 'Recurring Issues (from NGO Reports & Social Media)',
        'add_case_title': 'Add New Case or Site (Data Entry Simulation)',
        'case_location': 'Administrative Location of Case',
        'case_lat': 'Latitude',
        'case_lon': 'Longitude',
        'case_type': 'Entry Type',
        'submit_case': 'Submit Entry',
        'complaint_title': 'Complaints and Feedback Box',
        'complaint_type': 'Complaint/Report Type',
        'complaint_details': 'Complaint Details (lack of chlorine, new case requiring ambulance, etc.)',
        'submit_complaint': 'Submit Complaint (via WhatsApp Simulation)',
        'success_case': 'Case/Site added successfully.',
        'success_complaint': 'Complaint received successfully. An alert will be sent to relevant authorities.',
        'risk_high': 'High Risk (Epidemic Threshold Exceeded)',
        'risk_medium': 'Medium Risk (Intense Monitoring)',
        'risk_low': 'Low Risk (Stable)',
        'alert_box_high': '🚨 URGENT ALERT: Risk threshold exceeded in areas (A, B, C). Immediate response scale-up recommended.',
        'alert_box_medium': '⚠️ Warning: Slight increase in cases in area (D). Recommend increased water quality surveillance.',
        'alert_box_low': '✅ Status Stable: No critical risk indicators currently present.',
        'pbi_title': 'Power BI Dashboard: Comprehensive & Advanced Analysis',
    }
}
# دالة للحصول على النصوص باللغة المحددة
def _(key):
    return T[st.session_state.language].get(key, key)

# --- 3. التصميم (Styling & CSS Injection) ---
def apply_custom_styles():
    """حقن CSS لتطبيق تصميم Glass UI الأنيق والوضع الليلي/النهاري."""
    mode_class = 'dark-mode' if st.session_state.dark_mode else 'light-mode'

    css = f"""
    <style>
        /* إعدادات الخلفية العامة وتأثير التمرير */
        .stApp {{
            background: {'#111827' if st.session_state.dark_mode else '#f0f2f6'};
            transition: background-color 0.3s;
        }}

        /* تصميم Glass UI للعناصر/الحاويات */
        div[data-testid*="stBlock"],
        div[data-testid*="stBlock"] {{
            background: rgba({'30, 41, 59' if st.session_state.dark_mode else '255, 255, 255'}, 0.75);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, {'0.3' if st.session_state.dark_mode else '0.1'});
            border: 1px solid rgba({'49, 58, 70' if st.session_state.dark_mode else '255, 255, 255'}, 0.3);
            transition: all 0.3s;
        }}

        /* الأزرار المدورة والأنيقة */
        .stButton>button, .stDownloadButton>button {{
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            font-weight: bold;
            transition: background-color 0.3s, transform 0.1s;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover {{
            background-color: #2563eb;
            transform: translateY(-1px);
        }}
        
        /* تلوين النص الرئيسي في الوضع الليلي */
        .{mode_class} * {{
            color: {'#e5e7eb' if st.session_state.dark_mode else '#1f2937'} !important;
        }}
        
        /* استثناءات النص: العناوين الرئيسية */
        h1, h2, h3, h4, .stMarkdown, .stSelectbox label, .stTextInput label, .stDateInput label {{
            color: {'#ffffff' if st.session_state.dark_mode else '#111827'} !important;
        }}
        
        /* حقول الإدخال والـ Selectbox */
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"] {{
            border-radius: 8px;
        }}
        
        /* تلوين أزرار وضع الليل/النهار */
        .mode-toggle-btn {{
            background-color: {'#f9fafb' if st.session_state.dark_mode else '#1f2937'};
            color: {'#1f2937' if st.session_state.dark_mode else '#f9fafb'};
            border: 1px solid {'#4b5563' if st.session_state.dark_mode else '#d1d5db'};
        }}
        
        /* مؤشرات الخطر (KPI boxes) */
        .kpi-box {{
            text-align: center;
            padding: 10px 0;
            border-radius: 8px;
        }}
        .kpi-box h3 {{
            font-size: 1.25rem;
            margin: 0;
            opacity: 0.8;
        }}
        .kpi-box p {{
            font-size: 2rem;
            font-weight: bold;
            margin: 0;
        }}

        /* تباعد الأزرار في الشريط العلوي */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div:nth-child(2) .stButton,
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div:nth-child(3) .stButton {{
            margin-top: 25px; /* لضبط المحاذاة العمودية مع العنوان */
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(f'<div class="{mode_class}"></div>', unsafe_allow_html=True)


# --- 4. وظائف التفاعل والمنطق ---

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def toggle_language():
    st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
    st.rerun()

def get_risk_status():
    """يحدد مستوى الخطر بناءً على عدد الحالات (محاكاة لنظام EWS)."""
    total_cases = st.session_state.cholera_cases['Confirmed_Cases'].sum()
    if total_cases > 500:
        return 'High'
    elif total_cases > 200:
        return 'Medium'
    else:
        return 'Low'

def get_risk_color(risk_level):
    if risk_level == 'High':
        return 'red'
    elif risk_level == 'Medium':
        return 'orange'
    else:
        return 'green'

def add_new_case(location, lat, lon, case_type):
    """محاكاة إضافة بيانات جديدة إلى Supabase."""
    new_case = pd.DataFrame([{
        'Date': datetime.now().date(),
        'Confirmed_Cases': 1 if case_type == _('map_tooltip_case') else 0,
        'Deaths': 0,
        'Lat': lat,
        'Lon': lon,
        'Type': case_type,
        'Severity': 'Medium' # يمكن تخصيصها حسب النوع
    }])
    st.session_state.cholera_cases = pd.concat([st.session_state.cholera_cases, new_case], ignore_index=True)

# --- 5. واجهة المستخدم (UI Components) ---

def sidebar_controls():
    """إنشاء الأزرار الجانبية لاختيار المنطقة ومستوى الإنذار."""
    with st.sidebar:
        # Note: Language and Mode toggles are moved to the top header.
        
        # اختيار المنطقة (محاكاة)
        st.selectbox(_('region_select'), ['الخرطوم', 'كسلا', 'بورتسودان', 'الفاشر'], index=0)

        # عرض مستوى الإنذار الحالي
        risk_level = get_risk_status()
        risk_color = get_risk_color(risk_level)

        st.markdown(f"### **{_('risk_level')}**")
        st.markdown(
            f"""
            <div style='background-color: {risk_color}; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;'>
                {T[st.session_state.language][f'risk_{risk_level.lower()}']}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.info("💡 " + _('alert_box_high') if risk_level == 'High' else _('alert_box_medium') if risk_level == 'Medium' else _('alert_box_low'))


def render_map(df_cases, sites_data):
    """إنشاء وعرض الخريطة التفاعلية (Folium)."""
    # مركز افتراضي للخريطة
    m = folium.Map(location=[12.65, 15.05], zoom_start=7, tiles="cartodbdarkmatter" if st.session_state.dark_mode else "OpenStreetMap")

    # 1. طبقة خريطة الحرارة (Heatmap) للحالات المؤكدة
    case_coords = df_cases[['Lat', 'Lon']].values.tolist()
    HeatMap(case_coords, name="خريطة حرارة الحالات").add_to(m)

    # 2. طبقة الحالات المؤكدة (نقاط باللون الأحمر/البرتقالي حسب الخطورة)
    for index, row in df_cases.iterrows():
        color = 'red' if row['Severity'] == 'High' else 'orange' if row['Severity'] == 'Medium' else 'green'
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"{_('map_tooltip_case')}: {row['Type']} | {row['Date']}"
        ).add_to(m)

    # 3. طبقة عينات المياه الإيجابية (نقاط زرقاء)
    water_samples = df_cases[df_cases['Type'] == 'Positive Water Sample']
    for index, row in water_samples.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            icon=folium.Icon(color='blue', icon='tint', prefix='fa'),
            tooltip=f"{_('map_tooltip_water')} - {row['Date']}"
        ).add_to(m)

    # 4. طبقة مواقع توزيع الكلور (نقاط خضراء)
    for site in sites_data['Chlorine_Distribution']:
        folium.Marker(
            location=[site['Lat'], site['Lon']],
            icon=folium.Icon(color='green', icon='check', prefix='fa'),
            tooltip=f"{_('map_tooltip_chlorine')} ({site['Status']})"
        ).add_to(m)
        
    # 5. طبقة مخيمات النازحين (نقاط بنفسجية)
    for site in sites_data['IDP_Camps']:
        folium.Marker(
            location=[site['Lat'], site['Lon']],
            icon=folium.Icon(color='purple', icon='users', prefix='fa'),
            tooltip=f"{_('map_tooltip_idp')} - {site['Population']} people"
        ).add_to(m)

    # إضافة التحكم بالطبقات
    folium.LayerControl().add_to(m)

    # عرض الخريطة
    folium_static(m, width=700, height=500)


def kpis_and_chart(df_cases):
    """عرض مؤشرات الأداء الرئيسية (KPIs) والرسم البياني اليومي."""
    df_grouped = df_cases.groupby('Date')['Confirmed_Cases'].sum().reset_index()

    total_cases = df_cases['Confirmed_Cases'].sum()
    total_deaths = df_cases['Deaths'].sum()
    pos_water_samples = df_cases[df_cases['Type'] == 'Positive Water Sample'].shape[0]

    # KPIs in columns
    col1, col2, col3 = st.columns(3)
    
    # KPI 1
    with col1:
        st.markdown(
            f"""
            <div class='kpi-box' style='border-left: 5px solid #ef4444;'>
                <h3>{_('total_cases')}</h3>
                <p style='color: #ef4444;'>{total_cases}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # KPI 2
    with col2:
        st.markdown(
            f"""
            <div class='kpi-box' style='border-left: 5px solid #7c3aed;'>
                <h3>{_('total_deaths')}</h3>
                <p style='color: #7c3aed;'>{total_deaths}</p>
            </div>
            """, unsafe_allow_html=True)

    # KPI 3
    with col3:
        st.markdown(
            f"""
            <div class='kpi-box' style='border-left: 5px solid #22c55e;'>
                <h3>{_('pos_water_samples')}</h3>
                <p style='color: #22c55e;'>{pos_water_samples}</p>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("---")

    # Line Chart for Cases Trend
    st.subheader(_('cases_chart_title'))
    fig = px.line(
        df_grouped,
        x='Date',
        y='Confirmed_Cases',
        title=_('cases_chart_title'),
        labels={'Confirmed_Cases': _('total_cases'), 'Date': 'التاريخ' if st.session_state.language == 'ar' else 'Date'},
        template='plotly_dark' if st.session_state.dark_mode else 'plotly_white',
        line_shape='spline'
    )
    fig.update_traces(line=dict(color='#3b82f6', width=3))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def main_dashboard():
    """عرض لوحة التحكم الرئيسية (الخريطة والبيانات)."""
    
    col_map, col_pbi = st.columns([0.5, 0.5], gap="large")

    with col_map:
        st.subheader(_('map_title'))
        render_map(st.session_state.cholera_cases, st.session_state.sites_data)

    with col_pbi:
        st.subheader(_('pbi_title'))
        # تضمين لوحة Power BI باستخدام الكود المقدم
        power_bi_embed_html = """
        <iframe title="Cholera intelligent Dashboard(CID)" width="100%" height="500px" 
            src="https://app.powerbi.com/view?r=eyJrIjoiNmQ1M2I2NTQtZmJmYi00NTg0LWJhNmYtYWFjYTU0ZTlhYzMwIiwidCI6IjUxZTM3NGE2LTI3YWYtNDIwYi1iMGEyLTRkYTYyZDkzNWZjYyIsImMiOjZ9" 
            frameborder="0" allowFullScreen="true" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </iframe>
        """
        components.html(power_bi_embed_html, height=520)
        
    # KPIs and Chart section
    kpis_and_chart(st.session_state.cholera_cases)


def ews_analysis_tab():
    """عرض لوحة الإنذار المبكر والتحليل الذكي (محاكاة AI)."""
    st.header(_('ews_tab'))
    
    col_pred, col_analysis = st.columns(2, gap="large")

    with col_pred:
        st.subheader(_('prediction_title'))
        
        # محاكاة نتائج التنبؤ (نص/قائمة)
        # 7-day Prediction
        st.markdown(f"**{_('prediction_7d')}**")
        st.info("منطقة (أ): احتمالية 75%، منطقة (ب): احتمالية 60%")
        
        # 30-day Prediction
        st.markdown(f"**{_('prediction_30d')}**")
        st.warning("منطقة (ج): خطر مستدام، منطقة (د): مراقبة المياه الجوفية")

    with col_analysis:
        st.subheader(_('analysis_title'))

        # محاكاة تحليل النصوص والتقارير
        st.markdown(f"**{_('recurring_issues')}**")
        
        # قائمة المشكلات المستخلصة تلقائياً (محاكاة)
        issues = [
            "نقص حاد في نقاط توزيع الكلور في المربع 5.",
            "إفادة عن تلوث مصدر مياه رئيسي بمنطقة النازحين (س).",
            "مطالبات متكررة بتوفير فرق استجابة سريعة في مناطق ريفية."
        ]
        
        st.markdown("<ul>" + "".join([f"<li>{issue}</li>" for issue in issues]) + "</ul>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### **توجيهات التدخل الآلي**")
        st.success("""
        **توجيه آلي (للخطر العالي):**
        1. إرسال فريق تحقيق سريع (RRT) إلى منطقة (أ) للتحقق من مصدر التلوث خلال 24 ساعة.
        2. تخصيص شاحنات مياه معالجة بالكلور لمنطقة (ب) لمدة 72 ساعة.
        3. إصدار نشرة إرشادية عاجلة تستهدف مخيم (س).
        """)

def reporting_complaints_tab():
    """عرض لوحة إدخال البيانات والإبلاغ عن الشكاوى."""
    st.header(_('reporting_tab'))
    
    col_data_entry, col_complaint = st.columns(2, gap="large")

    # --- نموذج إضافة حالة/موقع جديد ---
    with col_data_entry:
        with st.form("case_entry_form"):
            st.subheader(_('add_case_title'))
            location = st.text_input(_('case_location'))
            case_type = st.selectbox(_('case_type'), [_('map_tooltip_case'), _('map_tooltip_water'), _('map_tooltip_chlorine')])
            
            # حقول خطوط الطول والعرض مع قيم وهمية أولية
            lat = st.number_input(_('case_lat'), value=12.70, format="%.4f")
            lon = st.number_input(_('case_lon'), value=15.15, format="%.4f")

            submitted = st.form_submit_button(_('submit_case'))
            if submitted and location and lat and lon:
                add_new_case(location, lat, lon, case_type)
                st.success(_('success_case'))
                st.rerun()

    # --- صندوق الشكاوى (محاكاة الواتساب) ---
    with col_complaint:
        with st.form("complaint_form"):
            st.subheader(_('complaint_title'))
            
            # محاكاة صندوق شكاوى الواتساب
            complaint_type = st.selectbox(_('complaint_type'), ['نقص كلور', 'حالة جديدة تستدعي الإسعاف', 'تلوث مياه', 'مشكلة صرف صحي'])
            details = st.text_area(_('complaint_details'), max_chars=300)
            contact = st.text_input("رقم الهاتف (اختياري)")
            
            submitted_complaint = st.form_submit_button(_('submit_complaint'))
            if submitted_complaint and details:
                # محاكاة إرسال الشكوى
                st.success(_('success_complaint'))
                # يمكن هنا إضافة منطق لتخزين الشكوى في Supabase أو إرسال تنبيه
                
# --- 6. تشغيل التطبيق الرئيسي ---
if __name__ == "__main__":
    
    # تطبيق الأنماط المخصصة أولاً
    apply_custom_styles()
    
    # إعداد الشريط الجانبي (يجب أن يتم استدعاؤه قبل أي شيء في الـ main content)
    sidebar_controls()

    # --- الشريط العلوي (Header) الجديد ---
    # تقسيم الشريط العلوي: العنوان (كبير) والزراين (صغير)
    header_col1, header_col2, header_col3 = st.columns([8, 1, 1], gap="small")

    with header_col1:
        # العنوان الرئيسي والفرعي
        st.markdown(f"""
            <div style="padding-top: 15px;">
                <h1>{_('title')}</h1>
                <p style="opacity: 0.7; margin-top: -10px;">{_('subtitle')}</p>
            </div>
            """, unsafe_allow_html=True)

    with header_col2:
        # زر تبديل اللغة (Language Switch)
        # استخدام st.markdown مع ارتفاع مخصص لمحاذاة الزر عمودياً
        st.markdown('<div style="height: 100%;">', unsafe_allow_html=True)
        if st.button(_('lang_switch'), key="header_lang_switch"):
            toggle_language()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    with header_col3:
        # زر تبديل الوضع الليلي/النهاري (Dark/Light Mode)
        mode_text = _('mode_switch_light') if st.session_state.dark_mode else _('mode_switch')
        mode_icon = '☀️' if st.session_state.dark_mode else '🌙'
        
        st.markdown('<div style="height: 100%;">', unsafe_allow_html=True)
        if st.button(f"{mode_icon} {mode_text}", key="header_mode_switch"):
            toggle_dark_mode()
            # لا نحتاج لـ rerun إذا كانت التغييرات تتم عبر CSS فقط، لكن لضمان تحديث Folium/Plotly نستخدمها
            st.rerun() 
        st.markdown('</div>', unsafe_allow_html=True)

    # فاصل أفقي أنيق تحت الشريط العلوي
    st.markdown("<hr style='border-top: 1px solid rgba(150, 150, 150, 0.2); margin-top: 0px; margin-bottom: 0px;'>", unsafe_allow_html=True)
    # --- نهاية الشريط العلوي ---

    
    # نظام التبويبات الرئيسي
    tab_dashboard, tab_ews, tab_reporting = st.tabs([_('dashboard_tab'), _('ews_tab'), _('reporting_tab')])

    with tab_dashboard:
        main_dashboard()

    with tab_ews:
        ews_analysis_tab()

    with tab_reporting:
        reporting_complaints_tab()
