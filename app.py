import streamlit as st
import streamlit.components.v1 as components

# --- الإعدادات العامة ---
st.set_page_config(page_title="Saudi Pumps | Smart Interlock", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stMetric { 
        background: linear-gradient(135deg, #0d1117 0%, #071a11 100%);
        border: 1px solid #1a7a4d; border-radius: 12px; padding: 20px;
    }
    h1 { color: #f0f6fc; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

if 'dest_level' not in st.session_state: st.session_state.dest_level = 0.5

# --- القائمة الجانبية مع منطق الربط ---
with st.sidebar:
    st.markdown("<h2 style='color: #1a7a4d;'>SAUDI PUMPS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    source_level = st.slider("مستوى خزان الإمداد T1", 0.0, 5.0, 4.2)
    
    # تفعيل الـ Bypass
    bypass_active = st.toggle("تفعيل المسار البديل (Bypass Path)", value=False)
    
    # إذا اشتغل الـ Bypass، الخط الرئيسي يقفل تماماً (100% انسداد)
    if bypass_active:
        main_valve_clog = 100
        st.warning("⚠️ المسار الرئيسي مغلق الآن (Interlock Active)")
    else:
        main_valve_clog = st.slider("انسداد الصمام الرئيسي %", 0, 100, 25)

    if st.button("إعادة تعيين T2"):
        st.session_state.dest_level = 0.0

# --- حسابات التدفق ---
flow_rate = 12.0 if bypass_active else (12.0 * (1 - main_valve_clog/100))
if flow_rate > 0:
    st.session_state.dest_level = min(5.0, st.session_state.dest_level + (flow_rate / 2500))

# --- الواجهة ---
st.markdown("<h1>نظام التحكم التبادلي الذكي | Saudi Pumps</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("معدل التدفق الحالي", f"{flow_rate:.2f} L/m")
m2.metric("حالة الصمام الرئيسي", "مغلق تماماً" if bypass_active else f"{main_valve_clog}%")
m3.metric("مستوى تعبئة T2", f"{(st.session_state.dest_level/5*100):.1f}%")

# --- الرسم الهندسي التفاعلي ---
def render_interlock_pid(t1, t2, main_clog, bypass, flow):
    main_v_color = "#ff4b4b" if bypass or main_clog > 90 else "#7a5a1a"
    bp_v_color = "#00ff88" if bypass else "#444"
    anim_speed = "2s" # سرعة ثابتة للمحاكاة
    
    svg = f"""
    <div style="display: flex; justify-content: center; background: #0b0e14; padding: 25px; border-radius: 20px; border: 1px solid #1a7a4d;">
    <svg width="850" height="400" viewBox="0 0 850 400">
        <rect x="50" y="100" width="90" height="200" fill="none" stroke="#1a7a4d" stroke-width="3" rx="5"/>
        <rect x="50" y="{300 - (t1/5*200)}" width="90" height="{(t1/5*200)}" fill="#1a7a4d" opacity="0.5"/>
        <text x="55" y="90" fill="#fff" font-size="12">ST-101</text>

        <rect x="700" y="100" width="90" height="200" fill="none" stroke="#1a7a4d" stroke-width="3" rx="5"/>
        <rect x="700" y="{300 - (t2/5*200)}" width="90" height="{(t2/5*200)}" fill="#1a7a4d" opacity="0.5"/>
        <text x="705" y="90" fill="#fff" font-size="12">ST-102</text>

        <path d="M140 250 H230 M310 250 H380 V180 H620 M380 250 V320 H620 M620 180 V250 H700 M620 320 V250" 
              stroke="#2d2d2d" stroke-width="10" fill="none"/>

        <g>
            {f'<circle r="4" fill="#00ff88"><animateMotion path="M140 250 H230 M310 250 H380 V180 H620 V250 H700" dur="{anim_speed}" repeatCount="indefinite" /></circle>' if not bypass and main_clog < 100 else ''}
            
            {f'<circle r="4" fill="#00ff88"><animateMotion path="M140 250 H230 M310 250 H380 V320 H620 V250 H700" dur="{anim_speed}" repeatCount="indefinite" /></circle>' if bypass else ''}
        </g>

        <circle cx="270" cy="250" r="35" fill="#05140b" stroke="#fff" stroke-width="2"/>
        <text x="255" y="255" fill="#fff" font-size="10">P-101</text>

        <rect x="470" y="170" width="40" height="20" fill="{main_v_color}" stroke="#fff"/>
        <text x="450" y="165" fill="#fff" font-size="10">الصمام الرئيسي</text>

        <rect x="470" y="310" width="40" height="20" fill="{bp_v_color}" stroke="#fff"/>
        <text x="450" y="305" fill="{bp_v_color}" font-size="10">صمام الـ Bypass</text>
    </svg>
    </div>
    """
    return svg

components.html(render_interlock_pid(source_level, st.session_state.dest_level, main_valve_clog, bypass_active, flow_rate), height=450)
