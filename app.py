import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ---------- CONFIGURE PAGE ----------
st.set_page_config(page_title="Amazon Listing AI Demo", page_icon="🛍️", layout="wide")

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #FF9900;'>
        🛍️ Amazon Listing AI Demo
    </h1>
    <p style='text-align: center; font-size:18px; color:#333333;'>
        Generate sample Amazon titles, bullet points & product summaries in seconds.
    </p>
    """,
    unsafe_allow_html=True,
)

# ---------- LOAD GEMINI API ----------
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------- FUNCTION TO GENERATE TEXT ----------
def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ✏️ Enter Your Product Keyword")
    keyword = st.text_input("Example: wireless mouse, yoga mat, water bottle")
    generate_btn = st.button("✨ Generate Sample Listing", use_container_width=True)

with col2:
    st.markdown("### 📦 AI Generated Output")
    output_placeholder = st.empty()

# ---------- SESSION TRACKER ----------
if "demo_used" not in st.session_state:
    st.session_state.demo_used = False

# ---------- MAIN LOGIC ----------
if generate_btn:
    if not keyword.strip():
        st.warning("⚠️ Please enter a product keyword.")
    elif not st.session_state.demo_used:
        with st.spinner("Generating amazing Amazon listing... 🪄"):
            time.sleep(1)
            try:
                prompt = f"Generate 2 catchy titles, 3 bullet points, and 1 short product summary for an Amazon listing about: {keyword}."
                result = generate_text(prompt)
                st.session_state.demo_used = True

                with output_placeholder.container():
                    # Product Image (Placeholder)
                    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=180)
                    st.markdown(
                        f"<div style='color:#222;padding:10px;background-color:#F9F9F9;border-radius:12px;'>"
                        f"{result}</div>",
                        unsafe_allow_html=True,
                    )
                    st.success("✅ Liked the sample? Hire me for full professional Amazon listings!")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("⚠️ You have reached the free demo limit. Hire me for the full version.")

# ---------- FOOTER ----------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray;'>
        Made with ❤️ using Streamlit & Gemini AI
    </p>
    """,
    unsafe_allow_html=True,
)
