import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Create model instance

model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")



# Streamlit App Title
st.title("🤖 Amazon AI Product Research Tool (Gemini)")

st.write("Enter a product keyword below to generate AI-powered product insights!")

# Input field for keyword
keyword = st.text_input("🔍 Enter Product Keyword:")

if st.button("Generate Insights"):
    if not keyword:
        st.warning("⚠️ Please enter a product keyword first.")
    else:
        with st.spinner("Analyzing your product..."):
            prompt = f"""
            Analyze the product keyword '{keyword}' and provide:
            1. Product Summary
            2. 3 Optimized Title Ideas
            3. 3 Bullet Points
            4. 1 Short Description
            """
            response = model.generate_content(prompt)
            st.success("✅ Analysis Complete!")
            st.write(response.text)
