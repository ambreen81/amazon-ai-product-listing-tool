import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Configure Gemini API
genai.configure(api_key=api_key)

# Create model instance (lighter, faster, less quota use)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit App Title
st.title("🤖 Amazon AI Product Research Tool (Gemini)")

st.write("Enter a product keyword below to generate AI-powered Amazon insights!")

# Input field for keyword
keyword = st.text_input("🔍 Enter Product Keyword:")

# When button is clicked
if st.button("Generate Insights"):
    if not keyword:
        st.warning("⚠️ Please enter a product keyword first.")
    else:
        with st.spinner("Analyzing your product... Please wait ⏳"):
            # Optimized, lightweight prompt
            prompt = f"""
            Provide Amazon product insights for '{keyword}' including:
            1. Brief product summary
            2. 2 optimized title ideas
            3. 3 key bullet points
            4. 1 short product description
            """

            # Generate AI response with error handling
            try:
                response = model.generate_content(prompt)
                st.success("✅ Analysis Complete!")
                st.write(response.text)
            except Exception as e:
                st.error(
                    "⚠️ The AI service is currently busy or your API quota has been exceeded. "
                    "Please try again later or use a new Gemini API key."
                )
