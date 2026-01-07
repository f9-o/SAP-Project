import streamlit as st
import streamlit.components.v1 as components

# --- 1. الهوية البصرية القصوى (The Ultimate Blueprint UX/UI) ---
st.set_page_config(page_title="Saudi Pumps V1.0 | Blueprint UI", layout="wide")

st.markdown("""
    <style>
    /* تحويل الخلفية إلى ورق مخططات هندسي كحلي */
    .main { 
        background-color: #001a2c;
        background-image: 
            linear-gradient(rgba(255,255,255,.05) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(255,255,255,.05) 1.5px, transparent 1.5px);
        background-size: 40px 40px;
    }
    /* تنسيق الكروت والمقاييس */
    .stMetric { 
        background: rgba(0, 45, 75, 0.6);
        border: 1px solid #005f99; 
        border-radius: 2px; padding: 20px;
        box-shadow: inset 0 0 10px rgba(0, 150, 255, 0.1);
    }
    h1, h2, h3 { 
        font-family: 'Consolas', 'Courier New', monospace; 
        color: #89d4ff; text-align: left; 
        text-transform: uppercase; letter-spacing: 2px;
        border-bottom: 1px solid #005f99;
        padding-bottom: 10px;
    }
    .diag-box {
        padding: 20px; border: 1px solid #005f99; background: rgba(0, 30, 50, 0.8);
        border-radius: 0px; font-family: 'Consolas'; color: #89d4ff; 
        direction: ltr; line-height: 1.6;
    }
    /* تنسيق السلايدر ليتناسب مع الهوية */
    .stSlider > div > div > div > div { background-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الحالة (Engineering Logic Engine) ---
if 'dest_level' not in st.session_state: st.session_state.dest_level = 0.5

with st.sidebar:
    st.markdown("<h2 style='border:none; color:#00d4ff;'>SAUDI PUMPS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#5da9d6; font-size:12px;'>SYSTEM VERSION: 1.0.0-PRO</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    s_level = st.slider("SOURCE TANK (LIT-01)", 0.0, 5.0, 4.2)
    mode = st.radio("OPERATION MODE", ["STANDARD (GLV-01)", "BYPASS (GLV-02)"])
    
    bypass_active = (mode == "BYPASS (GLV-02)")
    valve_pos = 0 if bypass_active else st.slider("VALVE POSITION (THROTTLE %)", 0, 100, 85)
    
    if st.button("SYSTEM TOTAL RESET"): st.session_state.dest_level = 0.0

# الحسابات الهيدروليكية (Bernoulli Simulation)
base_flow = 19.2 
flow_calc = base_flow if bypass_active else (base_flow * (valve_pos/100))
pressure_psi = (flow_calc * 1.15) if flow_calc > 0 else 0
st.session_state.dest_level = min(5.0, st.session_state.dest_level + (flow_calc / 5000))

# --- 3. لوحة التحكم (Main Dashboard) ---
st.markdown("<h1>[DWG-001] SYSTEM REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("FLOW (FIT-01)", f"{flow_calc:.1f} L/m")
c2.metric("PRESSURE (PIT-01)", f"{pressure_psi:.1f} PSI")
c3.metric("VALVE SIG", "OPEN" if flow_calc > 0 else "CLOSED")
c4.metric("DEST TANK (LIT-02)", f"{(st.session_state.dest_level/5*100):.1f}%")

# --- 4. المخطط الهندسي الحي (Dynamic Blueprint Simulation) ---
def render_blueprint_sim(t1, t2, bp, flow_val):
    flow_anim = "inline" if flow_val > 0 else "none"
    speed = max(0.5, 3.5 - (flow_val/6))
    
    return f"""
    <div style="background: #001a2c; padding: 30px; border: 1px solid #005f99; display: flex; justify-content: center;">
    <svg width="850" height="380" viewBox="0 0 850 380" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.5"/>
            </pattern>
            <filter id="neon_glow"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        <rect x="60" y="80" width="110" height="220" fill="none" stroke="#00d4ff" stroke-width="2"/>
        <rect x="60" y="{300 - (t1/5*220)}" width="110" height="{(t1/5*220)}" fill="#00d4ff" opacity="0.15"/>
        <text x="60" y="70" fill="#89d4ff" font-family="monospace" font-size="12">ST-101 (SOURCE)</text>

        <rect x="680" y="80" width="110" height="220" fill="none" stroke="#00d4ff" stroke-width="2"/>
        <rect x="680" y="{300 - (t2/5*220)}" width="110" height="{(t2/5*220)}" fill="#00d4ff" opacity="0.15"/>
        <text x="680" y="70" fill="#89d4ff" font-family="monospace" font-size="12">ST-102 (DEST)</text>

        <path d="M170 260 H240 M315 260 H390 V150 H610 M390 260 V330 H610 M610 150 V260 H680 M610 330 V260" 
              stroke="#004d80" stroke-width="8" fill="none" />
        
        <g style="display: {flow_anim};">
            <circle r="4" fill="#00ffcc" filter="url(#neon_glow)">
                <animateMotion path="{"M170 260 H390 V330 H610 V260 H680" if bp else "M170 260 H390 V150 H610 V260 H680"}" 
                dur="{speed}s" repeatCount="indefinite" />
            </circle>
        </g>

        <circle cx="277" cy="260" r="38" fill="#001a2c" stroke="#00d4ff" stroke-width="2"/>
        <path d="M255 260 L299 260 M277 238 L277 282" stroke="#00d4ff" stroke-width="1.5">
            <animateTransform attributeName="transform" type="rotate" from="0 277 260" to="360 277 260" dur="1.2s" repeatCount="indefinite" />
        </path>
        <text x="255" y="315" fill="#00d4ff" font-family="monospace" font-size="10">P-101 (12VDC)</text>

        <polygon points="190,250 215,270 215,250 190,270" fill="none" stroke="#fff" stroke-width="1.5"/> 
        
        <g transform="translate(485, 150)">
            <polygon points="-15,-10 15,10 15,-10 -15,10" fill="{"#ff3333" if bp else "none"}" stroke="#00d4ff" stroke-width="2"/>
            <circle cx="0" cy="0" r="3" fill="#00d4ff"/>
            <text x="-25" y="-20" fill="#89d4ff" font-size="9">GLV-01</text>
        </g>

        <g transform="translate(485, 330)">
            <polygon points="-15,-10 15,10 15,-10 -15,10" fill="{"none" if bp else "#003344"}" stroke="{"#00ffcc" if bp else "#444"}" stroke-width="2"/>
            <circle cx="0" cy="0" r="3" fill="{"#00ffcc" if bp else "#444"}"/>
            <text x="-25" y="-20" fill="{"#00ffcc" if bp else "#444"}" font-size="9">GLV-02 (BYPASS)</text>
        </g>
    </svg>
    </div>
    """
components.html(render_blueprint_sim(s_level, st.session_state.dest_level, bypass_active, flow_calc), height=410)

# --- 5. التقارير الفنية (Technical Logs) ---
st.markdown("<h3>[SCH-002] ENGINEERING LOGS & SPECIFICATIONS</h3>", unsafe_allow_html=True)
col_l, col_r = st.columns(2)

with col_l:
    st.markdown(f"""
    <div class="diag-box">
    // SYSTEM DIAGNOSTICS<br>
    STATUS: {"EMERGENCY_BYPASS_ENGAGED" if bypass_active else "NOMINAL_OPERATION"}<br>
    VELOCITY: {flow_calc/60:.4f} M/S<br>
    CONTROL_UNIT: ESP32_V1_WIFI_ENABLED<br>
    COMM_PROT: HTTP/WEBSOCKET_ACTIVE
    </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown("""
    <div class="diag-box">
    // MECHANICAL DATA<br>
    PUMP: CENTRIFUGAL P-101<br>
    PIPING: PVC SCH-40 (ID: 0.5")<br>
    INSTRUMENTATION: ULTRASONIC LIT, FLOW FIT<br>
    VALVE_TYPE: GLOBE (THROTTLING CAPABLE)
    </div>
    """, unsafe_allow_html=True)
