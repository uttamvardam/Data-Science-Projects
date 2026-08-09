"""
VROOM Cars — AI Vehicle Damage Detection
A professional Streamlit dashboard powered by a fine-tuned ResNet50 model.
"""
import os
import streamlit as st
from model_helper import predict

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="VROOM Cars | AI Damage Detection",
    page_icon="🏎️",
    layout="wide"
)

# =====================================================
# CLASS METADATA
# =====================================================
CLASS_INFO = {
    "Front Breakage": {"icon": "💥", "color": "#EF4444", "bg": "rgba(239,68,68,0.12)",
                        "border": "rgba(239,68,68,0.25)", "severity": "Severe", "area": "Front",
                        "advice": "Structural breakage detected. Immediate professional inspection recommended.",
                        "desc": "Major structural breakage on the front section, possibly affecting the frame, engine bay, or safety components."},
    "Front Crushed":  {"icon": "🔧", "color": "#F59E0B", "bg": "rgba(245,158,11,0.12)",
                        "border": "rgba(245,158,11,0.25)", "severity": "Moderate", "area": "Front",
                        "advice": "Front-end crush damage detected. Repair estimate recommended.",
                        "desc": "The front bumper or hood shows signs of moderate crush damage from impact."},
    "Front Normal":   {"icon": "✅", "color": "#22C55E", "bg": "rgba(34,197,94,0.12)",
                        "border": "rgba(34,197,94,0.25)", "severity": "None", "area": "Front",
                        "advice": "No damage detected at the front of the vehicle.",
                        "desc": "The front of the vehicle shows no signs of damage and appears fully intact."},
    "Rear Breakage":  {"icon": "💥", "color": "#EF4444", "bg": "rgba(239,68,68,0.12)",
                        "border": "rgba(239,68,68,0.25)", "severity": "Severe", "area": "Rear",
                        "advice": "Severe structural damage detected on the rear. Immediate professional inspection is strongly recommended before driving.",
                        "desc": "Structural breakage detected on the rear section of the vehicle."},
    "Rear Crushed":   {"icon": "🔧", "color": "#F59E0B", "bg": "rgba(245,158,11,0.12)",
                        "border": "rgba(245,158,11,0.25)", "severity": "Moderate", "area": "Rear",
                        "advice": "Moderate rear crush damage identified. A professional repair assessment is advised..",
                        "desc": "Moderate crush damage on the rear bumper or trunk area."},
    "Rear Normal":    {"icon": "✅", "color": "#22C55E", "bg": "rgba(34,197,94,0.12)",
                        "border": "rgba(34,197,94,0.25)", "severity": "None", "area": "Rear",
                        "advice": "No visible damage detected on the rear. Vehicle appears to be in good condition.",
                        "desc": "Rear of the vehicle appears undamaged and intact."},
}


# =====================================================
# CUSTOM CSS (DARK THEME)
# =====================================================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{ background:#0F1117; color:#F1F5F9; }
.block-container{ max-width:1180px; padding-top:0.5rem; padding-bottom:1rem; }

/* NAVBAR */
.navbar{ display:flex; align-items:center; justify-content:space-between;
    padding:14px 8px 18px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:26px; }
.nav-logo{ display:flex; align-items:center; gap:12px; }
.nav-logo-mark{ width:42px; height:42px; background:linear-gradient(135deg,#3B82F6,#6366F1);
    border-radius:11px; display:flex; align-items:center; justify-content:center;
    box-shadow:0 4px 14px rgba(99,102,241,0.35); position:relative; }
.nav-logo-mark::before{ content:''; position:absolute; inset:2px; border-radius:9px;
    border:1.5px solid rgba(255,255,255,0.15); }
.nav-brand-main{ font-size:20px; font-weight:900; color:#fff; letter-spacing:-0.3px; line-height:1; }
.nav-brand-main span{ color:#818CF8; }
.nav-brand-sub{ font-size:10.5px; color:#64748B; font-weight:600; letter-spacing:1.2px; margin-top:3px; text-transform:uppercase; }
.nav-links{ display:flex; gap:28px; font-size:13.5px; color:#94A3B8; font-weight:500; }
.nav-badge{ font-size:11px; font-weight:700; background:linear-gradient(135deg,#3B82F6,#6366F1);
    color:#fff; padding:5px 14px; border-radius:20px; letter-spacing:0.5px; }

/* HERO */
.hero-wrap{ position:relative; padding:36px 0 20px; overflow:hidden; }
.hero-bg{ position:absolute; inset:0;
    background: radial-gradient(ellipse 80% 60% at 60% 40%, rgba(99,102,241,0.10) 0%, transparent 70%),
                radial-gradient(ellipse 50% 40% at 20% 30%, rgba(59,130,246,0.08) 0%, transparent 60%);
    pointer-events:none; }
.hero-tag{ display:inline-flex; align-items:center; gap:8px;
    background:rgba(99,102,241,0.10); border:1px solid rgba(99,102,241,0.20);
    color:#A5B4FC; font-size:11px; font-weight:700; padding:6px 14px; border-radius:20px;
    letter-spacing:1.5px; text-transform:uppercase; margin-bottom:20px; }
.hero-title{ font-size:44px; font-weight:900; line-height:1.1; color:#fff; margin-bottom:18px; }
.hero-title span{ background:linear-gradient(135deg,#3B82F6,#8B5CF6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-desc{ font-size:15px; color:#94A3B8; line-height:1.7; max-width:460px; margin-bottom:22px; }
.hero-trust{ display:flex; align-items:center; gap:14px; margin-top:22px; font-size:13px; color:#64748B; }
.trust-dots{ display:flex; }
.trust-dot{ width:30px; height:30px; border-radius:50%; border:2px solid #0F1117; margin-left:-8px;
    display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff; }
.trust-dot:first-child{ margin-left:0; }
.hero-visual-card{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:20px; padding:26px; text-align:center; position:relative; }
.hero-car-icon{ font-size:80px; display:block; margin:0 auto 8px;
    filter:drop-shadow(0 0 25px rgba(99,102,241,0.4)); animation:float 4s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.damage-badges{ display:flex; justify-content:center; gap:6px; flex-wrap:wrap; margin-top:10px; }
.dmg-tag{ font-size:10.5px; padding:3px 10px; border-radius:20px; font-weight:600; }
.mini-grid{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:14px; }
.mini-card{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:12px; padding:12px 14px; display:flex; align-items:center; gap:10px; }
.mini-icon{ width:32px; height:32px; border-radius:8px; display:flex;
    align-items:center; justify-content:center; font-size:14px; flex-shrink:0; }
.mini-val{ font-size:15px; font-weight:800; color:#fff; line-height:1; }
.mini-lbl{ font-size:10.5px; color:#475569; font-weight:500; margin-top:2px; }

/* STATS BAR */
.stats-bar{ background:rgba(255,255,255,0.02); border-top:1px solid rgba(255,255,255,0.07);
    border-bottom:1px solid rgba(255,255,255,0.07); display:flex; margin:26px 0 0; }
.stat{ flex:1; text-align:center; padding:22px 12px; border-right:1px solid rgba(255,255,255,0.07); }
.stat:last-child{ border-right:none; }
.stat-val{ font-size:26px; font-weight:900; background:linear-gradient(135deg,#3B82F6,#8B5CF6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.stat-lbl{ font-size:11px; color:#334155; font-weight:600;
    text-transform:uppercase; letter-spacing:0.6px; margin-top:4px; }

/* SECTIONS */
.section-header{ text-align:center; margin:70px 0 32px; }
.section-eyebrow{ font-size:11px; font-weight:800; letter-spacing:2px;
    text-transform:uppercase; color:#6366F1; margin-bottom:10px; }
.section-title{ font-size:34px; font-weight:800; color:#fff; margin-bottom:10px; line-height:1.15; }
.section-desc{ 
    font-size:15px; 
    color:#94A3B8; 
    max-width:560px; 
    margin-left:auto; 
    margin-right:auto; 
    text-align:center; 
    display:block;
}

/* PIPELINE */
.pipe-wrap{ background:rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.07);
    border-radius:22px; padding:40px 28px; }
.pipe-label{ text-align:center; font-size:12px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:#64748B; margin-bottom:32px; }
.pipe-row{ display:flex; align-items:flex-start; justify-content:center; flex-wrap:wrap; }
.pipe-step{ display:flex; flex-direction:column; align-items:center; width:120px; text-align:center; }
.pipe-icon{ width:56px; height:56px; border-radius:14px;
    display:flex; align-items:center; justify-content:center; font-size:22px; margin-bottom:10px; }
.pipe-title{ font-size:13px; font-weight:700; color:#E2E8F0; }
.pipe-sub{ font-size:11px; color:#475569; margin-top:3px; }
.pipe-arrow{ color:#334155; font-size:18px; margin-top:18px; padding:0 6px; }

/* DAMAGE CLASS CARDS */
.dmg-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.dmg-card{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:16px; padding:22px 18px; text-align:center; transition:all 0.25s; }
.dmg-card:hover{ border-color:rgba(99,102,241,0.35);
    background:rgba(99,102,241,0.04); transform:translateY(-3px); }
.dmg-card-icon{ font-size:30px; margin-bottom:10px; }
.dmg-card-name{ font-size:14px; font-weight:700; color:#E2E8F0; margin-bottom:6px; }
.dmg-card-desc{ font-size:11.5px; color:#475569; line-height:1.5; }
.dmg-card-tag{ display:inline-block; font-size:10px; font-weight:700;
    padding:3px 10px; border-radius:20px; margin-top:10px;
    text-transform:uppercase; letter-spacing:0.5px; }

/* FEATURES */
.feat-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.feat-card{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:18px; padding:24px 22px; transition:all 0.25s; }
.feat-card:hover{ border-color:rgba(99,102,241,0.25); transform:translateY(-3px);
    box-shadow:0 20px 40px rgba(0,0,0,0.25); }
.feat-icon{ width:42px; height:42px; border-radius:11px;
    display:flex; align-items:center; justify-content:center;
    font-size:19px; margin-bottom:16px; }
.feat-title{ font-size:15px; font-weight:700; color:#F1F5F9; margin-bottom:8px; }
.feat-desc{ font-size:13px; color:#475569; line-height:1.6; }

/* UPLOAD TOOL */
.tool-header{ background:rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.07);
    border-bottom:none; border-radius:20px 20px 0 0;
    padding:22px 28px; display:flex; align-items:center; gap:14px; }
.tool-icon{ width:40px; height:40px;
    background:linear-gradient(135deg,rgba(59,130,246,0.2),rgba(99,102,241,0.2));
    border:1px solid rgba(99,102,241,0.3); border-radius:10px;
    display:flex; align-items:center; justify-content:center; font-size:17px; color:#818CF8; }
.tool-title{ font-size:16px; font-weight:700; color:#F1F5F9; }
.tool-sub{ font-size:12px; color:#475569; margin-top:2px; }
.tool-body-wrap{ background:rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.07);
    border-top:none; border-radius:0 0 20px 20px; padding:26px 28px 28px; }

[data-testid="stFileUploader"]{ background:rgba(99,102,241,0.03);
    border:2px dashed rgba(99,102,241,0.25) !important;
    border-radius:14px !important; padding:16px !important; }
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small{ color:#94A3B8 !important; }
[data-testid="stFileUploader"] button{
    background:linear-gradient(135deg,#3B82F6,#6366F1) !important;
    color:#fff !important; border:none !important; font-weight:600 !important; }

.stButton>button{ width:100%; height:52px; border:none; border-radius:12px;
    background:linear-gradient(135deg,#3B82F6,#6366F1); color:white; font-size:15px; font-weight:700;
    box-shadow:0 4px 24px rgba(99,102,241,0.28); transition:all 0.25s; }
.stButton>button:hover{ transform:translateY(-1px);
    box-shadow:0 6px 30px rgba(99,102,241,0.42);
    background:linear-gradient(135deg,#3B82F6,#6366F1); color:white; }

.file-info{ background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:14px 16px; height:100%; }
.file-info-row{ display:flex; justify-content:space-between; align-items:center;
    font-size:12.5px; color:#64748B; padding:7px 0; border-bottom:1px dashed rgba(255,255,255,0.05); }
.file-info-row:last-child{ border-bottom:none; }
.file-info-row b{ color:#E2E8F0; font-size:12.5px; }

.result-card{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:16px; padding:26px; margin-top:20px; }
.result-head{ display:flex; align-items:center; gap:14px; margin-bottom:22px;
    padding-bottom:18px; border-bottom:1px solid rgba(255,255,255,0.05); }
.res-icon{ width:52px; height:52px; border-radius:14px; display:flex;
    align-items:center; justify-content:center; font-size:22px; }
.res-title{ font-size:20px; font-weight:800; color:#F1F5F9; }
.res-sub{ font-size:13px; color:#475569; margin-top:3px; }
.verdict-row{ display:flex; align-items:center; justify-content:space-between;
    background:rgba(255,255,255,0.02); border-radius:12px; padding:14px 18px; margin-bottom:22px;
    border:1px solid rgba(255,255,255,0.05); }
.sev-badge{ font-size:12px; font-weight:700; padding:6px 14px; border-radius:20px; }
.conf-big{ font-size:28px; font-weight:900; }
.conf-title{ font-size:11px; font-weight:700; color:#64748B;
    text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px; }
.prob-row{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.prob-label{ font-size:12.5px; font-weight:600; color:#CBD5E1; width:160px; flex-shrink:0; }
.prob-track{ flex:1; height:8px; background:rgba(255,255,255,0.05); border-radius:10px; overflow:hidden; }
.prob-fill{ height:100%; border-radius:10px; transition:width 0.8s ease; }
.prob-pct{ font-size:12.5px; font-weight:700; color:#818CF8; width:48px; text-align:right; }
.meta-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:20px; }
.meta-card{ background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05);
    border-radius:10px; padding:12px 14px; }
.meta-lbl{ font-size:10px; color:#334155; font-weight:700;
    text-transform:uppercase; letter-spacing:0.6px; margin-bottom:4px; }
.meta-val{ font-size:14px; font-weight:700; color:#E2E8F0; }

/* FOOTER */
.footer{ padding:36px 0 20px; margin-top:60px;
    border-top:1px solid rgba(255,255,255,0.07);
    display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:36px; }
.footer-brand p{ font-size:13px; color:#334155; line-height:1.7; margin-top:12px; max-width:280px; }
.footer-col h4{ font-size:11px; font-weight:700; color:#475569;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:14px; }
.footer-col a{ display:block; font-size:13px; color:#64748B;
    text-decoration:none; margin-bottom:9px; }
.footer-bottom{ text-align:center; padding:22px 0 10px; color:#334155; font-size:12.5px;
    border-top:1px solid rgba(255,255,255,0.04); margin-top:30px; }

@media(max-width:900px){
    .dmg-grid, .feat-grid{ grid-template-columns:1fr 1fr; }
    .footer{ grid-template-columns:1fr 1fr; }
    .hero-title{ font-size:32px; }
    .section-title{ font-size:26px; }
    .meta-grid{ grid-template-columns:1fr 1fr; }
    .stats-bar{ flex-wrap:wrap; }
    .stat{ flex:0 0 50%; border-bottom:1px solid rgba(255,255,255,0.07); }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# NAVBAR
# =====================================================
navbar_html = (
    '<div class="navbar">'
    '<div class="nav-logo">'
    '<div class="nav-logo-mark">'
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
    '<path d="M3 13.5L4.5 8.5C4.8 7.6 5.6 7 6.5 7H17.5C18.4 7 19.2 7.6 19.5 8.5L21 13.5V17.5C21 17.8 20.8 18 20.5 18H19C18.7 18 18.5 17.8 18.5 17.5V16.5H5.5V17.5C5.5 17.8 5.3 18 5 18H3.5C3.2 18 3 17.8 3 17.5V13.5Z" fill="white"/>'
    '<circle cx="7" cy="14" r="1.5" fill="#1E40AF"/>'
    '<circle cx="17" cy="14" r="1.5" fill="#1E40AF"/>'
    '</svg>'
    '</div>'
    '<div>'
    '<div class="nav-brand-main">VROOM <span>Cars</span></div>'
    '<div class="nav-brand-sub">AI Damage Inspector</div>'
    '</div>'
    '</div>'
    '<div class="nav-links">'
    '<span>How It Works</span><span>Damage Types</span>'
    '<span>Features</span><span>Try It</span>'
    '</div>'
    '<span class="nav-badge">ResNet50 v1.0</span>'
    '</div>'
)
st.markdown(navbar_html, unsafe_allow_html=True)


# =====================================================
# HERO
# =====================================================
st.markdown('<div class="hero-wrap"><div class="hero-bg"></div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1.1, 1])

with col_l:
    hero_left_html = (
        '<div class="hero-tag">🤖 AI-Powered Detection</div>'
        '<div class="hero-title">Detect Vehicle Damage with '
        '<span>80% Accuracy</span> Using Deep Learning</div>'
        '<p class="hero-desc">VROOM Cars\' ResNet50-powered system classifies front & rear '
        'vehicle damage across 6 categories in seconds — helping insurers, fleets, and '
        'dealerships make faster, data-driven decisions.</p>'
        '<div class="hero-trust">'
        '<div class="trust-dots">'
        '<div class="trust-dot" style="background:linear-gradient(135deg,#3B82F6,#6366F1);">V</div>'
        '<div class="trust-dot" style="background:linear-gradient(135deg,#8B5CF6,#EC4899);">R</div>'
        '<div class="trust-dot" style="background:linear-gradient(135deg,#06B6D4,#3B82F6);">O</div>'
        '<div class="trust-dot" style="background:linear-gradient(135deg,#10B981,#06B6D4);">M</div>'
        '</div>'
        '<span>Trusted by <b style="color:#94A3B8;">automotive</b> professionals worldwide</span>'
        '</div>'
    )
    st.markdown(hero_left_html, unsafe_allow_html=True)

with col_r:
    hero_right_html = (
        '<div class="hero-visual-card">'
        '<span class="hero-car-icon">🚙</span>'

        # 3×2 GRID — forced with inline styles
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:360px;margin:16px auto 0;">'

        # Row 1 — Front classes
        '<span class="dmg-tag" style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);color:#F87171;text-align:center;">Front Breakage</span>'
        '<span class="dmg-tag" style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.25);color:#FBBF24;text-align:center;">Front Crushed</span>'
        '<span class="dmg-tag" style="background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.25);color:#4ADE80;text-align:center;">Front Normal</span>'

        # Row 2 — Rear classes
        '<span class="dmg-tag" style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);color:#F87171;text-align:center;">Rear Breakage</span>'
        '<span class="dmg-tag" style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.25);color:#FBBF24;text-align:center;">Rear Crushed</span>'
        '<span class="dmg-tag" style="background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.25);color:#4ADE80;text-align:center;">Rear Normal</span>'

        '</div>'
        '</div>'

        '<div class="mini-grid">'
        '<div class="mini-card"><div class="mini-icon" style="background:rgba(59,130,246,0.12);color:#60A5FA;">⚡</div>'
        '<div><div class="mini-val">&lt; 2s</div><div class="mini-lbl">Inference Time</div></div></div>'
        '<div class="mini-card"><div class="mini-icon" style="background:rgba(34,197,94,0.12);color:#4ADE80;">✓</div>'
        '<div><div class="mini-val">≈ 80%</div><div class="mini-lbl">Accuracy</div></div></div>'
        '<div class="mini-card"><div class="mini-icon" style="background:rgba(245,158,11,0.12);color:#FBBF24;">🏷️</div>'
        '<div><div class="mini-val">6</div><div class="mini-lbl">Damage Classes</div></div></div>'
        '<div class="mini-card"><div class="mini-icon" style="background:rgba(139,92,246,0.12);color:#A78BFA;">🗂️</div>'
        '<div><div class="mini-val">2.3K+</div><div class="mini-lbl">Training Images</div></div></div>'
        '</div>'
    )
    st.markdown(hero_right_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# STATS BAR
# =====================================================
stats_html = (
    '<div class="stats-bar">'
    '<div class="stat"><div class="stat-val">≈80%</div><div class="stat-lbl">Accuracy</div></div>'
    '<div class="stat"><div class="stat-val">6</div><div class="stat-lbl">Damage Classes</div></div>'
    '<div class="stat"><div class="stat-val">&lt; 2s</div><div class="stat-lbl">Per Inspection</div></div>'
    '<div class="stat"><div class="stat-val">2,300</div><div class="stat-lbl">Training Images</div></div>'
    '<div class="stat"><div class="stat-val">ResNet50</div><div class="stat-lbl">Architecture</div></div>'
    '</div>'
)
st.markdown(stats_html, unsafe_allow_html=True)


# =====================================================
# ADDITIONAL CSS FOR LIVE DEMO (add once, near your other CSS)
# =====================================================
st.markdown("""
<style>
/* ── LIVE DEMO ENHANCEMENTS ── */
.demo-wrap{
    background:linear-gradient(160deg, rgba(99,102,241,0.04), rgba(59,130,246,0.02));
    border:1px solid rgba(99,102,241,0.15);
    border-radius:24px;
    padding:0;
    margin-top:20px;
    overflow:hidden;
    box-shadow:0 20px 60px rgba(0,0,0,0.25);
}
.demo-header-pro{
    background:linear-gradient(135deg, rgba(59,130,246,0.08), rgba(99,102,241,0.05));
    border-bottom:1px solid rgba(255,255,255,0.06);
    padding:24px 32px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    flex-wrap:wrap;
}
.demo-header-left{ display:flex; align-items:center; gap:14px; }
.demo-icon-pro{
    width:48px; height:48px;
    background:linear-gradient(135deg,#3B82F6,#6366F1);
    border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:20px; color:#fff;
    box-shadow:0 6px 18px rgba(99,102,241,0.35);
}
.demo-title-pro{ font-size:17px; font-weight:800; color:#F1F5F9; letter-spacing:-0.2px; }
.demo-sub-pro{ font-size:12px; color:#64748B; margin-top:3px; }
.demo-status{
    display:flex; align-items:center; gap:8px;
    background:rgba(34,197,94,0.10);
    border:1px solid rgba(34,197,94,0.25);
    padding:6px 14px; border-radius:20px;
    font-size:11.5px; font-weight:700; color:#4ADE80;
    letter-spacing:0.5px;
}
.status-dot{
    width:8px; height:8px; border-radius:50%;
    background:#22C55E; box-shadow:0 0 8px rgba(34,197,94,0.6);
    animation:pulse-dot 2s infinite;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.4} }

.demo-body{ padding:32px; }

.upload-hint{
    text-align:center;
    color:#64748B;
    font-size:12.5px;
    margin-bottom:16px;
    display:flex; align-items:center; justify-content:center; gap:16px;
    flex-wrap:wrap;
}
.upload-hint span{
    display:inline-flex; align-items:center; gap:5px;
    font-weight:500;
}
.upload-hint .hint-dot{ color:#334155; }

.image-preview-frame{
    background:rgba(0,0,0,0.25);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:16px;
    padding:16px;
    margin:20px 0;
    position:relative;
}
.image-preview-label{
    position:absolute; top:14px; left:14px;
    background:rgba(15,17,23,0.85);
    backdrop-filter:blur(6px);
    color:#94A3B8;
    font-size:10.5px; font-weight:700;
    padding:5px 12px; border-radius:20px;
    letter-spacing:1px; text-transform:uppercase;
    border:1px solid rgba(255,255,255,0.08);
    z-index:2;
}
.image-preview-frame img{ border-radius:10px; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# LIVE DEMO — CLEAN PROFESSIONAL VERSION
# =====================================================
st.markdown("""
<style>
/* Demo Card Container */
.demo-card{
    background:rgba(255,255,255,0.025);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    margin-top:24px;
    overflow:hidden;
    box-shadow:0 20px 60px rgba(0,0,0,0.3);
}

/* Demo Header */
.demo-head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:22px 28px;
    background:linear-gradient(135deg, rgba(59,130,246,0.06), rgba(99,102,241,0.03));
    border-bottom:1px solid rgba(255,255,255,0.06);
    flex-wrap:wrap;
    gap:14px;
}
.demo-head-left{ display:flex; align-items:center; gap:14px; }
.demo-icon{
    width:44px; height:44px;
    background:linear-gradient(135deg,#3B82F6,#6366F1);
    border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:19px; color:#fff;
    box-shadow:0 6px 18px rgba(99,102,241,0.35);
}
.demo-h-title{ font-size:16px; font-weight:800; color:#F1F5F9; line-height:1.2; }
.demo-h-sub{ font-size:12px; color:#64748B; margin-top:3px; }
.demo-status{
    display:flex; align-items:center; gap:8px;
    background:rgba(34,197,94,0.10);
    border:1px solid rgba(34,197,94,0.25);
    padding:6px 14px; border-radius:20px;
    font-size:11px; font-weight:700; color:#4ADE80;
    letter-spacing:0.5px;
}
.status-dot{
    width:7px; height:7px; border-radius:50%;
    background:#22C55E;
    box-shadow:0 0 8px rgba(34,197,94,0.6);
    animation:pulse-dot 2s infinite;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* Demo Body */
.demo-body{ padding:28px; }

/* Info Row */
.info-row{
    display:flex;
    justify-content:center;
    gap:24px;
    margin-bottom:18px;
    flex-wrap:wrap;
    font-size:12px;
    color:#64748B;
}
.info-row span{
    display:inline-flex; align-items:center; gap:6px;
}
.info-row b{ color:#94A3B8; font-weight:600; }

/* File Uploader Overrides */
[data-testid="stFileUploader"]{
    background:rgba(99,102,241,0.04) !important;
    border:2px dashed rgba(99,102,241,0.25) !important;
    border-radius:14px !important;
    padding:14px !important;
}
[data-testid="stFileUploader"] section{
    background:transparent !important;
    border:none !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small{
    color:#94A3B8 !important;
}
[data-testid="stFileUploader"] button{
    background:linear-gradient(135deg,#3B82F6,#6366F1) !important;
    color:#fff !important;
    border:none !important;
    font-weight:600 !important;
    border-radius:8px !important;
}
/* Uploaded file preview inside uploader */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"]{
    background:rgba(255,255,255,0.03) !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:10px !important;
}
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *{
    color:#CBD5E1 !important;
}

/* Image Preview Section */
.preview-wrap{
    background:rgba(0,0,0,0.25);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:14px;
    padding:20px;
    margin:20px 0;
    text-align:center;
    position:relative;
}
.preview-tag{
    display:inline-block;
    background:rgba(99,102,241,0.15);
    color:#A5B4FC;
    font-size:10.5px; font-weight:700;
    padding:4px 12px; border-radius:20px;
    letter-spacing:1px; text-transform:uppercase;
    margin-bottom:16px;
    border:1px solid rgba(99,102,241,0.25);
}

/* Analyze Button */
.stButton>button{
    width:100% !important;
    height:52px !important;
    border:none !important;
    border-radius:12px !important;
    background:linear-gradient(135deg,#3B82F6,#6366F1) !important;
    color:white !important;
    font-size:15px !important;
    font-weight:700 !important;
    box-shadow:0 6px 24px rgba(99,102,241,0.35) !important;
    transition:all 0.25s !important;
    margin-top:8px !important;
}
.stButton>button:hover{
    transform:translateY(-2px) !important;
    box-shadow:0 10px 32px rgba(99,102,241,0.5) !important;
}

/* Result Card */
.result-card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;
    padding:24px;
    margin-top:20px;
}
.result-head{
    display:flex; align-items:center; gap:14px;
    margin-bottom:18px; padding-bottom:16px;
    border-bottom:1px solid rgba(255,255,255,0.06);
}
.res-icon{
    width:50px; height:50px; border-radius:13px;
    display:flex; align-items:center; justify-content:center;
    font-size:22px;
}
.res-title{ font-size:19px; font-weight:800; color:#F1F5F9; }
.res-sub{ font-size:13px; color:#64748B; margin-top:3px; line-height:1.5; }
.verdict-row{
    display:flex; align-items:center; justify-content:space-between;
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.05);
    border-radius:12px;
    padding:14px 18px;
}
.sev-badge{ font-size:12px; font-weight:700; padding:6px 14px; border-radius:20px; }
.conf-big{ font-size:28px; font-weight:900; }
</style>
""", unsafe_allow_html=True)


# Section header
demo_header_html = (
    '<div class="section-header" style="text-align:center; width:100%;">'
    '<div class="section-eyebrow">Live Demo</div>'
    '<div class="section-title">Try the AI Damage Detector</div>'
    '<p style="font-size:15px; color:#94A3B8; max-width:700px; margin:0 auto; text-align:center; display:block; padding:0 20px;">Upload a front or rear vehicle image to receive instant AI-powered damage analysis.</p>'
    '</div>'
)
st.markdown(demo_header_html, unsafe_allow_html=True)


# Card top: header
card_head_html = (
    '<div class="demo-card">'
    '<div class="demo-head">'
    '<div class="demo-head-left">'
    '<div class="demo-icon">🤖</div>'
    '<div>'
    '<div class="demo-h-title">AI Vehicle Inspector</div>'
    '<div class="demo-h-sub">Powered by ResNet50 · Deep Learning Model</div>'
    '</div>'
    '</div>'
    '<div class="demo-status"><span class="status-dot"></span>MODEL READY</div>'
    '</div>'
    '<div class="demo-body">'
)
st.markdown(card_head_html, unsafe_allow_html=True)

# Info bar
info_html = (
    '<div class="info-row">'
    '<span>📄 <b>JPG · PNG · JPEG</b></span>'
    '<span>📦 Max <b>200 MB</b></span>'
    '<span>🔒 <b>Processed Locally</b></span>'
    '</div>'
)
st.markdown(info_html, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload vehicle image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

image_path = None
analyze = False

if uploaded_file:
    image_path = "temp_file.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Preview
    st.markdown(
        '<div class="preview-wrap">'
        '<div class="preview-tag">🖼️ Image Preview</div>',
        unsafe_allow_html=True
    )
    _, img_col, _ = st.columns([1, 2, 1])
    with img_col:
        st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    analyze = st.button(
        "🚀  Analyze Vehicle Damage",
        key="analyze_btn",
        use_container_width=True,
        type="primary"
    )


# =====================================================
# PREDICTION RESULT
# =====================================================
if analyze and image_path:
    with st.spinner("🔍 Running ResNet50 inference..."):
        try:
            result = predict(image_path)
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

    class_name = result["class_name"]
    confidence = result["confidence"]
    info = CLASS_INFO[class_name]

    result_html = (
        '<div class="result-card">'
        '<div class="result-head">'
        f'<div class="res-icon" style="background:{info["bg"]};border:1px solid {info["border"]};color:{info["color"]};">{info["icon"]}</div>'
        '<div>'
        f'<div class="res-title">{class_name}</div>'
        f'<div class="res-sub">{info["advice"]}</div>'
        '</div>'
        '</div>'
        '<div class="verdict-row">'
        f'<span class="sev-badge" style="background:{info["bg"]};color:{info["color"]};">'
        f'{info["severity"]} Damage · {info["area"]} View'
        '</span>'
        f'<span class="conf-big" style="color:{info["color"]};">{confidence*100:.1f}%</span>'
        '</div>'
        '</div>'
    )
    st.markdown(result_html, unsafe_allow_html=True)

# Close demo-body + demo-card
st.markdown('</div></div>', unsafe_allow_html=True)
# =====================================================
# HOW IT WORKS
# =====================================================
how_header_html = (
    '<div class="section-header" style="text-align:center; width:100%;">'
    '<div class="section-eyebrow">Process</div>'
    '<div class="section-title">How Damage Analysis Works</div>'
    '<p style="font-size:15px; color:#94A3B8; max-width:700px; margin:0 auto; text-align:center; display:block; padding:0 20px;">From raw image to detailed damage report in under 2 seconds.</p>'
    '</div>'
)
st.markdown(how_header_html, unsafe_allow_html=True)

pipe_html = (
    '<div class="pipe-wrap">'
    '<div class="pipe-label">Damage Data Pipeline</div>'
    '<div class="pipe-row">'
    '<div class="pipe-step">'
    '<div class="pipe-icon" style="background:rgba(59,130,246,0.12);border:1px solid rgba(59,130,246,0.2);color:#60A5FA;">🖼️</div>'
    '<div class="pipe-title">Input Image</div><div class="pipe-sub">Photo / Web App</div>'
    '</div>'
    '<div class="pipe-arrow">›</div>'
    '<div class="pipe-step">'
    '<div class="pipe-icon" style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.2);color:#818CF8;">⚙️</div>'
    '<div class="pipe-title">Preprocessing</div><div class="pipe-sub">Resize · Normalize</div>'
    '</div>'
    '<div class="pipe-arrow">›</div>'
    '<div class="pipe-step">'
    '<div class="pipe-icon" style="background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.2);color:#A78BFA;">🧠</div>'
    '<div class="pipe-title">ResNet50 Model</div><div class="pipe-sub">Feature Extraction</div>'
    '</div>'
    '<div class="pipe-arrow">›</div>'
    '<div class="pipe-step">'
    '<div class="pipe-icon" style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.2);color:#FBBF24;">🏷️</div>'
    '<div class="pipe-title">Classification</div><div class="pipe-sub">Damage Analysis</div>'
    '</div>'
    '<div class="pipe-arrow">›</div>'
    '<div class="pipe-step">'
    '<div class="pipe-icon" style="background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.2);color:#4ADE80;">📄</div>'
    '<div class="pipe-title">Report</div><div class="pipe-sub">Result · Confidence</div>'
    '</div>'
    '</div>'
    '</div>'
)
st.markdown(pipe_html, unsafe_allow_html=True)


# =====================================================
# DAMAGE CLASSES (FIXED — single-line HTML)
# =====================================================
dmg_header_html = (
    '<div class="section-header" style="text-align:center; width:100%;">'
    '<div class="section-eyebrow">Detection Coverage</div>'
    '<div class="section-title">6 Vehicle Damage Classes Detected</div>'
    '<p style="font-size:15px; color:#94A3B8; max-width:700px; margin:0 auto; text-align:center; display:block; padding:0 20px;">Our model covers front and rear damage severity across all standard vehicle types.</p>'
    '</div>'
)
st.markdown(dmg_header_html, unsafe_allow_html=True)

cards_html = '<div class="dmg-grid">'
for cls_name, info in CLASS_INFO.items():
    cards_html += (
        '<div class="dmg-card">'
        f'<div class="dmg-card-icon">{info["icon"]}</div>'
        f'<div class="dmg-card-name">{cls_name}</div>'
        f'<div class="dmg-card-desc">{info["desc"]}</div>'
        f'<div class="dmg-card-tag" style="background:{info["bg"]};color:{info["color"]};">'
        f'{info["severity"]}'
        '</div>'
        '</div>'
    )
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)


# =====================================================
# FEATURES
# =====================================================
feat_header_html = (
    '<div class="section-header" style="text-align:center; width:100%;">'
    '<div class="section-eyebrow">Why VROOM Cars</div>'
    '<div class="section-title">Built for Accuracy & Speed</div>'
    '<p style="font-size:15px; color:#94A3B8; max-width:700px; margin:0 auto; text-align:center; display:block; padding:0 20px;">Everything you need for professional vehicle damage inspection at scale.</p>'
    '</div>'
)
st.markdown(feat_header_html, unsafe_allow_html=True)

features = [
    ("📷", "rgba(59,130,246,0.12)", "#60A5FA", "Image Quality Handling",
        "Robust preprocessing pipeline handles varied lighting, angles, and image sizes automatically."),
    ("🧠", "rgba(139,92,246,0.12)", "#A78BFA", "Deep Learning Model",
        "Fine-tuned ResNet50 backbone with unfrozen layer4 for optimal damage feature extraction."),
    ("📊", "rgba(34,197,94,0.12)", "#4ADE80", "Confidence Scores",
        "Every prediction includes full probability distribution across all 6 damage classes."),
    ("⚡", "rgba(245,158,11,0.12)", "#FBBF24", "Real-Time Inference",
        "Analyze vehicle damage in under 2 seconds directly in your browser via CPU inference."),
    ("🎯", "rgba(6,182,212,0.12)", "#22D3EE", "Severity Classification",
        "Distinguishes between Normal, Crushed, and Breakage severity for front & rear views."),
    ("🚗", "rgba(236,72,153,0.12)", "#F472B6", "Front & Rear Coverage",
        "Comprehensive coverage of both front and rear vehicle inspection angles."),
]

feat_html = '<div class="feat-grid">'
for icon, bg, color, title, desc in features:
    feat_html += (
        '<div class="feat-card">'
        f'<div class="feat-icon" style="background:{bg};color:{color};">{icon}</div>'
        f'<div class="feat-title">{title}</div>'
        f'<div class="feat-desc">{desc}</div>'
        '</div>'
    )
feat_html += '</div>'
st.markdown(feat_html, unsafe_allow_html=True)



# =====================================================
# FOOTER
# =====================================================
footer_html = (
    '<div class="footer">'
    '<div class="footer-brand">'
    '<div class="nav-logo">'
    '<div class="nav-logo-mark">'
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none">'
    '<path d="M3 13.5L4.5 8.5C4.8 7.6 5.6 7 6.5 7H17.5C18.4 7 19.2 7.6 19.5 8.5L21 13.5V17.5C21 17.8 20.8 18 20.5 18H19C18.7 18 18.5 17.8 18.5 17.5V16.5H5.5V17.5C5.5 17.8 5.3 18 5 18H3.5C3.2 18 3 17.8 3 17.5V13.5Z" fill="white"/>'
    '<circle cx="7" cy="14" r="1.5" fill="#1E40AF"/>'
    '<circle cx="17" cy="14" r="1.5" fill="#1E40AF"/>'
    '</svg>'
    '</div>'
    '<div>'
    '<div class="nav-brand-main">VROOM <span>Cars</span></div>'
    '<div class="nav-brand-sub">AI Damage Inspector</div>'
    '</div>'
    '</div>'
    '<p>AI-powered vehicle damage classification using deep learning. Detect front and rear damage from a single photo.</p>'
    '</div>'
    '<div class="footer-col"><h4>Product</h4>'
    '<a>Features</a><a>How It Works</a><a>Damage Types</a><a>Live Demo</a>'
    '</div>'
    '<div class="footer-col"><h4>Model</h4>'
    '<a>Architecture</a><a>Training Data</a><a>Performance</a><a>Classes</a>'
    '</div>'
    '<div class="footer-col"><h4>Technology</h4>'
    '<a>PyTorch</a><a>ResNet50</a><a>Streamlit</a><a>Deep Learning</a>'
    '</div>'
    '</div>'
    '<div class="footer-bottom">'
    '©2026 VROOM Cars · v1.0 · AI Damage Inspector · Built with Streamlit'
    '</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)