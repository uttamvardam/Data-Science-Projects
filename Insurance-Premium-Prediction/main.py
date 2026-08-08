import streamlit as st
from prediction_helper import predict
from PIL import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


# -------------------------------------
# Page Configuration
# -------------------------------------
st.set_page_config(
    page_title="Shield Insurance",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------
# Custom CSS
# -------------------------------------
st.markdown("""
<style>

.stApp{
    background-color:#F5F9FF;
}

/* Main Container */
.block-container{
    padding-top:1rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Navigation */
.navbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:white;
    padding:18px 30px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom:30px;
}

.logo{
    color:#1565C0;
    font-size:58px;
    font-weight:800;
    line-height:1.1;
}   
.tagline{
    color:gray;
    font-size:14px;
    margin-left:72px;   /* Align with "Shield Insurance" */
    margin-top:2px;
}
.menu{
    font-size:18px;
    color:#444;
}

/* Hero */
.hero-title{
    font-size:28px;
    font-weight:600;
    line-height:1.2;
}

.hero-blue{
    color:#1565C0;
}

.hero-text{
    color:#666;
    font-size:18px;
    margin-top:15px;
}

/* Form Card */
[data-testid="stForm"]{
    background:white;
    border-radius:20px;
    padding:30px;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

/* Button */
.stButton>button{
    width:100%;
    height:52px;
    border:none;
    border-radius:10px;
    background:#1565C0;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#0D47A1;
    color:white;
}

/* Metric Card */
[data-testid="stMetric"]{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}

/* Image */
.stImage img{
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------
# Navigation Bar
# -------------------------------------
st.markdown("""
<div class="navbar">

<div>
<div class="logo">🛡 Shield Insurance</div>
<div class="tagline">Protecting Your Future with AI</div>
</div>

<div class="menu">
🏠 Home &nbsp;&nbsp;&nbsp;
📋 Plans &nbsp;&nbsp;&nbsp;
📞 Support
</div>

</div>
""", unsafe_allow_html=True)

# -------------------------------------
# Hero Section
# -------------------------------------
left, right = st.columns([1.3,1])

with left:

    st.markdown("""
<div class="hero-title">

Protect Your Family with

<span class="hero-blue">

Shield Insurance

</span>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="hero-text">

Estimate your annual health insurance premium
using Artificial Intelligence.

</div>
""", unsafe_allow_html=True)

    st.markdown("##### ✅ AI Powered Prediction")
    st.markdown("##### ✅ Trusted Premium Estimates")
    st.markdown("##### ✅ Instant Results")
    st.markdown("##### ✅ Secure Information")

with right:
    image = Image.open(BASE_DIR / "assets" / "insurance.png")
    st.image(image, use_container_width=True)

st.divider()

# -------------------------------------
# Options
# -------------------------------------
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Overweight', 'Obesity', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Occasional', 'Regular'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Northeast', 'Southwest', 'Southeast'],
    'Medical History': [
        'No Disease',
        'Diabetes',
        'High blood pressure',
        'Diabetes & High blood pressure',
        'Thyroid',
        'Heart disease',
        'High blood pressure & Heart disease',
        'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# -------------------------------------
# Form Title
# -------------------------------------
st.markdown("""
<h2 style="text-align:center;color:#1565C0;">
Health Insurance Premium Estimator
</h2>

<p style="text-align:center;color:gray;">
Fill in your information below to estimate your annual insurance premium.
</p>
""", unsafe_allow_html=True)

# -------------------------------------
# Prediction Form
# -------------------------------------
with st.form("prediction_form"):

    st.subheader("👤 Personal Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

    with col2:
        gender = st.selectbox(
            "Gender",
            categorical_options["Gender"]
        )

    with col3:
        marital_status = st.selectbox(
            "Marital Status",
            categorical_options["Marital Status"]
        )

    st.divider()

    st.subheader("💼 Employment & Income")

    col1, col2, col3 = st.columns(3)

    with col1:
        income_lakhs = st.number_input(
            "Annual Income (Lakhs)",
            min_value=0,
            max_value=200,
            value=10
        )

    with col2:
        employment_status = st.selectbox(
            "Employment Status",
            categorical_options["Employment Status"]
        )

    with col3:
        number_of_dependants = st.number_input(
            "Dependants",
            min_value=0,
            max_value=20,
            value=0
        )

    st.divider()

    st.subheader("🏥 Health Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        bmi_category = st.selectbox(
            "BMI Category",
            categorical_options["BMI Category"]
        )

    with col2:
        smoking_status = st.selectbox(
            "Smoking Status",
            categorical_options["Smoking Status"]
        )

    with col3:
        medical_history = st.selectbox(
            "Medical History",
            categorical_options["Medical History"]
        )

    st.divider()

    st.subheader("🛡 Insurance Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        genetical_risk = st.select_slider(
            "Genetic Risk",
            options=[1,2,3,4,5],
            value=2,
            help="""
1 = Very Low Risk

2 = Low Risk

3 = Moderate Risk

4 = High Risk

5 = Very High Risk
"""
        )

    with col2:
        insurance_plan = st.selectbox(
            "Insurance Plan",
            categorical_options["Insurance Plan"],
            help="""
Bronze = Lowest Premium

Silver = Balanced Premium

Gold = Highest Premium
"""
        )

    with col3:
        region = st.selectbox(
            "Region",
            categorical_options["Region"]
        )

    st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "💰 Estimate Premium"
    )

# -------------------------------------
# Prediction
# -------------------------------------
if submitted:

    input_dict = {
        "Age": age,
        "Number of Dependants": number_of_dependants,
        "Income in Lakhs": income_lakhs,
        "Genetical Risk": genetical_risk,
        "Insurance Plan": insurance_plan,
        "Employment Status": employment_status,
        "Gender": gender,
        "Marital Status": marital_status,
        "BMI Category": bmi_category,
        "Smoking Status": smoking_status,
        "Region": region,
        "Medical History": medical_history
    }

    prediction = predict(input_dict)

    st.success("Premium Estimated Successfully!")

    st.markdown("## 💰 Estimated Annual Premium")

    st.metric(
        label="Insurance Premium",
        value=f"₹ {prediction:,.0f}"
    )


    # -------------------------------------
    # How Prediction Works
    # -------------------------------------

    st.divider()

    st.subheader("📊 Factors Used for Premium Estimation")

    factor1, factor2, factor3 = st.columns(3)

    with factor1:
        st.info("""
    ### 👤 Personal Factors

    - Age
    - Gender
    - Marital Status
    - Dependants
    - Annual Income
    """)

    with factor2:
        st.info("""
    ### ❤️ Health Factors

    - BMI Category
    - Smoking Status
    - Medical History
    - Genetic Risk
    """)

    with factor3:
        st.info("""
    ### 🛡 Insurance Factors

    - Insurance Plan
    - Employment Status
    - Region
    """)

    # -------------------------------------
    # Disclaimer
    # -------------------------------------

    st.warning(
        """
    **Disclaimer**

    The estimated premium is generated using a Machine Learning model and is intended for educational purposes only. Actual insurance premiums may vary depending on insurer policies, underwriting, and additional customer information.
    """
    )
