import streamlit as st
import os

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="Lauki Credit Bureau & Underwriting Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Custom CSS to Lock Streamlit Outer Container to Viewport
# This completely hides Streamlit's outer scrollbars, leaving ONLY 1 single scrollbar from the custom app!
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html, body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        min-height: 100% !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp {
        width: 100% !important;
        min-height: 100vh !important;
        overflow: visible !important;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    iframe {
        border: none !important;
        width: 100% !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Read and Render the Custom HTML Dashboard
# Upgraded: The iframe handles scrolling natively over the full screen height,
# and the outer Streamlit container is locked, completely eliminating double scrollbars!
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
html_path = os.path.join(current_dir, "index.html")

try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Render with scrolling=True so iframe handles the single vertical scrollbar natively!
    st.components.v1.html(
        html_content,
        height=3000,
        scrolling=True
    )

except Exception as e:
    st.error(f"Failed to load dashboard: {str(e)}")
