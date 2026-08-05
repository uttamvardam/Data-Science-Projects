import os
import streamlit as st
from model_helper import predict

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Vehicle Damage Detection",
    page_icon="🚗",
    layout="centered"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

/* Hide Streamlit Branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main Container */
.block-container{
    max-width:850px;
    padding-top:1.2rem;
    padding-bottom:1.2rem;
}

/* Background */
.stApp{
    background:#F8FAFC;
}

/* Hero Banner */
.hero{
    background:linear-gradient(135deg,#2563EB,#1D4ED8);
    color:white;
    padding:22px;
    border-radius:16px;
    text-align:center;
    margin-bottom:18px;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

.hero h1{
    margin:0;
    font-size:34px;
    font-weight:700;
}

.hero p{
    margin-top:6px;
    font-size:16px;
    opacity:.95;
}

/* Cards */
.card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:16px;
    margin-bottom:16px;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

/* File Uploader */
[data-testid="stFileUploader"]{
    border:2px dashed #CBD5E1;
    border-radius:12px;
    padding:10px;
}

/* Uploaded Image */
img{
    border-radius:12px;
}

/* Button */
.stButton>button{
    width:100%;
    height:48px;
    border:none;
    border-radius:10px;
    background:#2563EB;
    color:white;
    font-size:16px;
    font-weight:600;
}

.stButton>button:hover{
    background:#1D4ED8;
    color:white;
}

/* Prediction Result */
.result{
    background:#EFF6FF;
    border-left:5px solid #2563EB;
    border-radius:10px;
    padding:14px 16px;
    margin-top:10px;
}

.result h2{
    margin:0;
    color:#2563EB;
    font-size:28px;
}

.result p{
    margin:6px 0 0;
    color:#475569;
}

/* Metrics */
[data-testid="stMetric"]{
    border:1px solid #E5E7EB;
    border-radius:10px;
    padding:8px;
    background:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div class="hero">
    <h1>🚗 Vehicle Damage Detection</h1>
    <p>AI-powered vehicle damage classification using <b>ResNet50</b></p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# UPLOAD SECTION
# =====================================================

st.markdown("<h3 style='text-align: center;'>📤 Upload Vehicle Image</h3>", unsafe_allow_html=True)

image_path = None

uploaded_file = st.file_uploader(
    "Choose a JPG or PNG image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file:

    image_path = "temp_file.jpg"

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(
        uploaded_file,
        use_container_width=True
    )

    st.button(
        "🚀 Analyze Damage",
        key="analyze_btn",
        use_container_width=True,
        type="primary"
    )

    analyze = st.session_state.analyze_btn

else:
    analyze = False

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PREDICTION RESULT
# =====================================================

# =====================================================
# PREDICTION RESULT
# =====================================================
if analyze and image_path:
    with st.spinner("Analyzing vehicle image..."):
        try:
            prediction = predict(image_path)
        finally:
            # Clean up temporary file safely
            if os.path.exists(image_path):
                os.remove(image_path)

    with st.container(border=True):
        st.markdown(
            """
            <h3 style="
                text-align:center;
                margin:0 0 12px 0;
                color:#1E3A8A;">
                🔍 Prediction Result
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # Using st.html() or explicit single-line formatted markdown ensures raw HTML renders properly
        result_html = f"""
        <div class="result">
            <p style="margin:0; color:#64748B; font-size:14px;">
                Predicted Damage Class
            </p>
            <h2 style="margin:8px 0 0 0; color:#2563EB; font-weight:700;">
                🚗 {prediction}
            </h2>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)


# =====================================================
# MODEL INFORMATION
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("""
<h3 style="
text-align:center;
margin:0 0 15px 0;
color:#1E293B;">
🧠 Model Information
</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Architecture",
        value="ResNet50"
    )

    st.metric(
        label="Classes",
        value="6"
    )

with col2:
    st.metric(
        label="Training Images",
        value="2,300"
    )

    st.metric(
        label="Accuracy",
        value="≈80%"
    )

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DAMAGE CLASSES
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("""
<h3 style="
text-align:center;
margin:0 0 15px 0;
color:#1E293B;">
🚗 Damage Classes
</h3>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.info("Front Normal")
    st.info("Rear Normal")

with c2:
    st.warning("Front Crushed")
    st.warning("Rear Crushed")

with c3:
    st.error("Front Breakage")
    st.error("Rear Breakage")

st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# TIPS
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("""
<h3 style="
text-align:center;
margin:0 0 12px 0;
color:#1E293B;">
📸 Tips for Best Results
</h3>
""", unsafe_allow_html=True)

st.markdown("""
- Upload a **clear, high-quality** vehicle image.
- Use a **front** or **rear** vehicle view.
- Keep the damaged area clearly visible.
- Avoid blurry, dark, or cropped images.
""")

st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div style="
text-align:center;
color:#94A3B8;
font-size:13px;
margin-top:5px;
padding-bottom:5px;">
Vehicle Damage Detection • Streamlit • PyTorch
</div>
""", unsafe_allow_html=True)