import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Try connecting to Gemini API
try:
    genai.configure(api_key=api_key)

    # Try model 1 (latest version)
    try:
        test_model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
        test_model.generate_content("Hello")
        active_model = "models/gemini-2.0-flash-exp"
    except Exception:
        # Fallback model
        test_model = genai.GenerativeModel("models/gemini-1.5-flash")
        test_model.generate_content("Hello")
        active_model = "models/gemini-1.5-flash"

    # ✅ Stylish green status bar
    st.markdown(
        f"""
        <div style="
            background-color: #16a34a;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        ">
            ✅ System Status: Connected to Gemini ({active_model})
        </div>
        """,
        unsafe_allow_html=True,
    )

except Exception as e:
    # ❌ Red error bar
    st.markdown(
        f"""
        <div style="
            background-color: #dc2626;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
        ">
            ❌ System Status: Gemini Connection Failed!<br>{e}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()  # Stop execution if not connected

# App UI
st.title("🤖 Amazon AI Product Research Tool (Gemini)")
st.write("Enter a product keyword below to generate AI-powered Amazon insights!")

keyword = st.text_input("🔍 Enter Product Keyword:")

if st.button("Generate Insights"):
    if not keyword:
        st.warning("⚠️ Please enter a product keyword first.")
    else:
        with st.spinner("Analyzing your product... Please wait ⏳"):
            prompt = f"""
            Provide Amazon product insights for '{keyword}' including:
            1. Brief product summary
            2. 2 optimized title ideas
            3. 3 key bullet points
            4. 1 short product description
            """

            try:
                model = genai.GenerativeModel(active_model)
                response = model.generate_content(prompt)
                st.success("✅ Analysis Complete!")
                st.write(response.text)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
                st.info(
                    "💡 Tip: If this happens often, your API key might have reached its usage limit "
                    "or the Gemini service could be temporarily busy."
                )
