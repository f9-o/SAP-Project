import streamlit as st
import streamlit.components.v1 as components

# الإعدادات العامة للواجهة
st.set_page_config(page_title="SAUDI PUMPS Control Center", layout="wide")

# تنسيق CSS
st.markdown("""
    <style>
    .main { background-color: #040605; }
    .stMetric { 
        background-color: #0d1117; 
        border: 1px solid #1a7a4d; border-radius: 10px; padding: 15px;
    }
    h1, h2, h3 { color: #f0f6fc; font-family: 'Arial'; text-align: right; }
    .status-box { 
        padding: 20px; border-radius: 10px; border: 1px solid #1a7a4d; 
        background: #05140b; color: #e6edf3; direction: rtl; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

if 'dest_level' not in st.session_state: st.session_state.dest_level = 0.0

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>SAUDI PUMPS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    # التحكم في المحاكاة
    main_clog = st.slider("إغلاق صمام الخط الرئيسي (Main Line Gate Valve %)", 0, 100, 20)
    bypass_open = st.checkbox("فتح صمام المسار البديل (Bypass Gate Valve)")
    t1_level = st.slider("مستوى خزان الإمداد ST-101 (m)", 0.0, 5.0, 4.0)
    
    if st.button("إعادة تعيين (Reset System)"):
        st.session_state.dest_level = 0.0

# حسابات التدفق بناءً على التعديلات الهندسية الجديدة
# المسار الرئيسي يقل بالانسداد، والمسار البديل يضيف تدفقاً إذا فُتح صمام البوابة فيه
flow_main = 10.0 * (1 - main_clog/100)
flow_bypass = 8.0 if bypass_open else 0.0
total_flow = flow_main + flow_bypass

# تحديث مستوى الخزان الثاني
st.session_state.dest_level = min(5.0, st.session_state.dest_level + (total_flow / 2000))

# العرض العلوي
st.markdown("<h1 style='text-align: center;'>مركز التحكم والمراقبة المطور | SAUDI PUMPS</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("معدل التدفق الكلي (Total Flow)", f"{total_flow:.2f} L/m")
c2.metric("حالة الخط الرئيسي", "منسد" if main_clog > 80 else "طبيعي")
c3.metric("مستوى T2", f"{(st.session_state.dest_level/5*100):.1f} %")

# رسم الـ P&ID المطور بجميع الصمامات المطلوبة
def get_industrial_pid(t1, t2, main_clg, bypass):
    bp_color = "#00ff88" if bypass else "#444"
    return f"""
    <div style="display: flex; justify-content: center; background: #0d1117; padding: 20px; border-radius: 15px; border: 1px solid #1a7a4d;">
    <svg width="900" height="400" viewBox="0 0 900 400">
        <rect x="50" y="100" width="80" height="180" fill="none" stroke="#1a7a4d" stroke-width="3"/>
        <rect x="50" y="{280 - (t1/5*180)}" width="80" height="{(t1/5*180)}" fill="#1a7a4d" opacity="0.5"/>
        <rect x="75" y="105" width="30" height="8" fill="cyan"/> <text x="40" y="90" fill="#fff" font-size="12">ST-101 (Level Sensor)</text>

        <path d="M130 250 H180" stroke="#1a7a4d" stroke-width="4"/>
        <polygon points="140,240 160,260 160,240 140,260" fill="white" stroke="white"/>
        <text x="135" y="235" fill="#aaa" font-size="9">Gate V1</text>

        <path d="M180 250 H240" stroke="#1a7a4d" stroke-width="4"/>
        <polygon points="200,240 220,260 220,240 200,260" fill="white" stroke="white"/>
        <text x="195" y="235" fill="#aaa" font-size="9">Gate V2</text>

        <circle cx="280" cy="250" r="30" fill="#05140b" stroke="#fff" stroke-width="2"/>
        <text x="265" y="255" fill="#fff" font-size="10" font-weight="bold">P-101</text>

        <path d="M310 250 H360" stroke="#1a7a4d" stroke-width="4"/>
        <polygon points="320,240 340,250 320,260" fill="none" stroke="gold" stroke-width="2"/>
        <text x="315" y="235" fill="gold" font-size="9">NRV (عدم رجوع)</text>

        <path d="M360 250 H420 V180 H600 M420 250 V320 H600" stroke="#1a7a4d" stroke-width="4" fill="none"/>
        
        <rect x="480" y="170" width="30" height="20" fill="#7a5a1a"/>
        <text x="460" y="165" fill="#fff" font-size="9">Main Gate V ({main_clg}%)</text>

        <rect x="480" y="310" width="30" height="20" fill="{bp_color}"/>
        <text x="460" y="305" fill="{bp_color}" font-size="9">Bypass Gate V</text>

        <path d="M600 180 V250 H720" stroke="#1a7a4d" stroke-width="4" fill="none"/>
        <path d="M600 320 V250" stroke="#1a7a4d" stroke-width="4" fill="none"/>

        <rect x="720" y="100" width="80" height="180" fill="none" stroke="#1a7a4d" stroke-width="3"/>
        <rect x="720" y="{280 - (t2/5*180)}" width="80" height="{(t2/5*180)}" fill="#1a7a4d" opacity="0.5"/>
        <rect x="745" y="105" width="30" height="8" fill="cyan"/> <text x="710" y="90" fill="#fff" font-size="12">ST-102 (Level Sensor)</text>
    </svg>
    </div>
    """

components.html(get_industrial_pid(source_level, st.session_state.dest_level, main_clog, bypass_open), height=450)

# شرح القطع المضافة (التوثيق)
st.markdown("---")
st.subheader("قائمة المعدات الهندسية المحدثة (Saudi Pumps Standard)")
st.markdown("""
<div class="status-box">
<b>1. Level Sensors (LIT-101/102):</b> تم إضافة حساسات فوق صوتية لكلا الخزانين لمراقبة الميزانية المائية بدقة.<br>
<b>2. Isolation Valves (Gate V1/V2):</b> صمامات عزل قبل وبعد المضخة لتسهيل عمليات الصيانة دون تفريغ الخزانات.<br>
<b>3. Non-Return Valve (NRV):</b> صمام عدم رجوع يمنع ارتداد الماء للمضخة عند التوقف، مما يحمي ريش المضخة من "المطرقة المائية".<br>
<b>4. Bypass System:</b> مسار بديل مزود بصمام بوابة يدوي لضمان استمرار التدفق في حال حدوث صيانة أو انسداد في الخط الرئيسي.
</div>
""", unsafe_allow_html=True)
