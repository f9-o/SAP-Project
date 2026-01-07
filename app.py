import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

# الإعدادات العامة للواجهة
st.set_page_config(page_title="SAUDI PUMPS Control Center", layout="wide")

# تنسيق CSS متقدم
st.markdown("""
    <style>
    .main { background-color: #040605; }
    .stMetric { 
        background: linear-gradient(135deg, #0d1117 0%, #05140b 100%);
        border: 1px solid #1a7a4d; border-radius: 10px; padding: 20px;
        box-shadow: 0 4px 15px rgba(26, 122, 77, 0.2);
    }
    h1, h2, h3 { color: #f0f6fc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: right; }
    .status-box { 
        padding: 20px; border-radius: 10px; border: 1px solid #1a7a4d; 
        background: rgba(5, 20, 11, 0.8); color: #e6edf3; direction: rtl; line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

if 'dest_level' not in st.session_state: st.session_state.dest_level = 0.0

with st.sidebar:
    # اللوجو التفاعلي المحدث
    st.markdown("""
        <div style="text-align: center;">
        <svg width="140" height="140" viewBox="0 0 200 200">
            <circle cx="100" cy="85" r="55" fill="none" stroke="#1a7a4d" stroke-width="6"/>
            <g transform="translate(100,85)">
                <path d="M-30 0 L30 0 M0 -30 L0 30" stroke="#ffffff" stroke-width="5">
                    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3s" repeatCount="indefinite" />
                </path>
                <circle r="8" fill="#1a7a4d"/>
            </g>
            <text x="100" y="165" fill="#ffffff" font-family="Arial" font-size="20" text-anchor="middle" font-weight="bold">SAUDI PUMPS</text>
        </svg>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    clog = st.slider("Gate Valve Obstruction (%)", 0, 100, 20)
    source_level = st.slider("Source Tank Level (m)", 0.0, 5.0, 4.0)
    if st.button("System Reset"):
        st.session_state.dest_level = 0.0

# الحسابات الهندسية
pump_pwm = min(100.0, 40.0 + (clog * 0.7))
solenoid_activation = 100.0 if clog > 65 else 0.0
flow_rate = (12.0 * (1 - clog/100)) + (pump_pwm/100 * 4.0) + (solenoid_activation/100 * 7.0)

# محاكاة امتلاء الخزان
st.session_state.dest_level = min(5.0, st.session_state.dest_level + (flow_rate / 2500))

# الواجهة الرئيسية
st.markdown("<h1 style='text-align: center;'>المنصة الوطنية للتحكم الصناعي | SAUDI PUMPS</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Flow Rate (L/m)", f"{flow_rate:.2f}")
col2.metric("Motor PWM (%)", f"{pump_pwm:.1f}")
col3.metric("T2 Level (%)", f"{(st.session_state.dest_level/5*100):.1f}")

# الرسم الهندسي الحي المطور (Animated P&ID)
def get_advanced_diagram(pwm, clg, sol, s_lvl, d_lvl, f_rate):
    sol_color = "#1a7a4d" if sol > 0 else "#2d2d2d"
    flow_speed = max(0.2, 3.0 - (f_rate / 5)) # التحكم في سرعة حركة جزيئات الماء
    
    svg = f"""
    <div style="display: flex; justify-content: center; background: #0d1117; padding: 25px; border-radius: 15px; border: 1px solid #1a7a4d;">
    <svg width="850" height="380" viewBox="0 0 850 380" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#1a7a4d; stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#05140b; stop-opacity:1" />
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>

        <rect x="50" y="80" width="100" height="200" fill="none" stroke="#1a7a4d" stroke-width="3"/>
        <rect x="50" y="{280 - (s_lvl/5*200)}" width="100" height="{(s_lvl/5*200)}" fill="url(#waterGrad)" />
        <text x="50" y="70" fill="#fff" font-size="12" font-weight="bold">ST-101 (T1)</text>

        <rect x="700" y="80" width="100" height="200" fill="none" stroke="#1a7a4d" stroke-width="3"/>
        <rect x="700" y="{280 - (d_lvl/5*200)}" width="100" height="{(d_lvl/5*200)}" fill="url(#waterGrad)" />
        <text x="700" y="70" fill="#fff" font-size="12" font-weight="bold">ST-102 (T2)</text>

        <path d="M150 250 H230 M305 250 H400 V180 H550 M400 250 V310 H550 M550 180 V250 H700 M550 310 V250" 
              stroke="#2d2d2d" stroke-width="10" fill="none" />
        
        {f'<circle r="3" fill="#00ff88" filter="url(#glow)"><animateMotion dur="{flow_speed}s" repeatCount="indefinite" path="M150 250 H230 M305 250 H400 V180 H550 M550 180 V250 H700" /></circle>' if f_rate > 0 else ''}
        {f'<circle r="3" fill="#00ff88" filter="url(#glow)"><animateMotion dur="{flow_speed}s" repeatCount="indefinite" path="M400 250 V310 H550 V250" /></circle>' if sol > 0 else ''}

        <g transform="translate(270, 250)">
            <circle cx="0" cy="0" r="35" fill="#05140b" stroke="#fff" stroke-width="3" filter="url(#glow)"/>
            <path d="M-20 0 L20 0 M0 -20 L0 20" stroke="#fff" stroke-width="3">
                <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{1/(pwm/20 + 0.1)}s" repeatCount="indefinite" />
            </path>
        </g>
        <text x="245" y="305" fill="#fff" font-size="11" font-weight="bold">P-101</text>

        <rect x="450" y="165" width="40" height="30" fill="#7a5a1a" stroke="#fff" />
        <text x="440" y="160" fill="#ffcc00" font-size="10">HV (Gate: {clg}%)</text>
        <rect x="450" y="295" width="40" height="30" fill="{sol_color}" stroke="#fff" />
        <text x="440" y="290" fill="#00ff88" font-size="10">XV (Solenoid)</text>

        <circle cx="620" cy="250" r="8" fill="gold" filter="url(#glow)" />
        <text x="590" y="240" fill="gold" font-size="10">Flow Sensor</text>
        <rect x="735" y="85" width="30" height="10" fill="cyan" />
        <text x="715" y="80" fill="cyan" font-size="10">Level Sensor</text>
    </svg>
    </div>
    """
    return svg

components.html(get_advanced_diagram(pump_pwm, clog, solenoid_activation, source_level, st.session_state.dest_level, flow_rate), height=420)

# التوثيق والبيانات الفنية
st.markdown("---")
t1, t2, t3 = st.tabs(["Strategic Objective", "Sensor Network", "Physical Integration"])

with t1:
    st.markdown("""
    <div class="status-box">
    <b>الهدف الاستراتيجي (Strategic Objective):</b><br>
    بناء نظام ضخ ذكي يعتمد على "التوأم الرقمي" (Digital Twin) لتقليل الانقطاعات الصناعية. يحلل النظام الفرق بين PWM المحرك والتدفق الفعلي؛ 
    فإذا اكتشف مقاومة عالية (انسداد)، يقوم بفتح مسار الطوارئ (XV) تلقائياً، مما يضمن استمرار العمليات في ST-102 وحماية P-101 من الإجهاد.
    </div>
    """, unsafe_allow_html=True)

with t2:
    st.markdown("""
    <div class="status-box">
    <b>شبكة الحساسات (Sensor Network):</b><br>
    - <b>Flow Sensor:</b> يراقب كفاءة النقل اللحظية (FIT).<br>
    - <b>Level Sensor:</b> مراقبة المخزون الاستراتيجي ومنع الفيضان (LIT).<br>
    - <b>Diagnostic Sensor:</b> مراقبة جهد التيار PWM في ESP32 للتنبؤ بالأعطال الميكانيكية قبل وقوعها.
    </div>
    """, unsafe_allow_html=True)

with t3:
    st.markdown("""
    <div class="status-box">
    <b>التوصيل الفيزيائي (Physical Setup):</b><br>
    1. ربط المضخة بـ <b>L298N Driver</b> للتحكم بالسرعة.<br>
    2. ربط Solenoid Valve بـ <b>Relay</b> يتم تفعيله برمجياً.<br>
    3. معالجة البيانات عبر <b>ESP32 Dual Core</b> لضمان استقرار قراءات الحساسات والتحكم.
    </div>
    """, unsafe_allow_html=True)