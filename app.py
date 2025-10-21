import streamlit as st

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"]


# Configure Gemini API
genai.configure(api_key=api_key)

# Create model instance

model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")



# Streamlit App Title
st.title("🤖 Amazon AI Product Research Tool (Gemini)")

st.write("Enter a product keyword below to generate AI-powered product insights!")

# Input field for keyword
keyword = st.text_input("🔍 Enter Product Keyword:")


import google.generativeai as genai

# -------------------------------
# 1. Load API Key from Streamlit Secrets
# -------------------------------
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# -------------------------------
# 2. Create Model Instance
# -------------------------------
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")

# -------------------------------
# 3. Streamlit App Layout
# -------------------------------
st.set_page_config(
    page_title="Amazon AI Product Research Tool",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Amazon AI Product Research Tool (Gemini)")
st.write("Generate AI-powered Amazon product insights quickly and professionally!")

# Input field for product keyword
keyword = st.text_input("🔍 Enter Product Keyword:")

# Optional: user can choose output detail level
detail_level = st.selectbox(
    "Choose Detail Level:",
    ["Basic", "Detailed"]
)

# -------------------------------
# 4. Generate Insights Button
# -------------------------------

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

            # Build prompt based on detail level
            if detail_level == "Basic":
                prompt = f"""
                Analyze the product keyword '{keyword}' and provide:
                1. Product Summary
                2. 3 Optimized Title Ideas
                3. 3 Bullet Points
                4. 1 Short Description
                Format the output with clear headings for each section.
                """
            else:
                prompt = f"""
                Provide a detailed analysis for the product keyword '{keyword}':
                1. Product Summary
                2. 3 Highly Optimized Title Ideas
                3. 5 Bullet Points Highlighting Key Features
                4. 1 Short Description
                5. Suggested Target Audience
                6. Competitor Analysis Highlights
                Format the output with clear headings for each section.
                """

            # Call Gemini API
            try:
                response = model.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_output_tokens=800
                )

                st.success("✅ Analysis Complete!")

                # Split response into sections based on headings
                output_text = response.output_text
                sections = output_text.split("\n")
                current_section = ""
                content_dict = {}

                for line in sections:
                    line_strip = line.strip()
                    if line_strip.endswith(":") or line_strip.startswith("1.") or line_strip.startswith("2.") \
                       or line_strip.startswith("3.") or line_strip.startswith("4.") \
                       or line_strip.startswith("5.") or line_strip.startswith("6."):
                        current_section = line_strip
                        content_dict[current_section] = ""
                    elif current_section:
                        content_dict[current_section] += line_strip + "\n"

                # Display sections with copy buttons
                for section, content in content_dict.items():
                    st.subheader(section)
                    st.text_area(label="", value=content.strip(), height=120)
                    st.button("📋 Copy to Clipboard", key=section, on_click=st.experimental_set_query_params, args=(content.strip(),))

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# -------------------------------
# 5. Footer
# -------------------------------
st.markdown("---")
st.markdown("Made with ❤️ using **Google Gemini API**")
