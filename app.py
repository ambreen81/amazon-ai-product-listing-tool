import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Create model instance
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")

# Streamlit app layout
st.title("Amazon Listing AI Demo")
st.subheader("Generate sample titles, bullet points & summary")
st.write("Enter your product keyword to see a small demo:")

# Input from user
keyword = st.text_input("Product Keyword:")

# Session state to track free demo usage
if "demo_used" not in st.session_state:
    st.session_state.demo_used = False

# Generate demo content
if st.button("Generate Sample Listing"):
    if not st.session_state.demo_used:
        # Generate titles
        titles = [
            f"{keyword} - High Quality & Affordable",
            f"Best {keyword} for Everyday Use",
            f"Top-rated {keyword} You’ll Love"
        ]

        # Generate bullet points
        bullets = [
            f"✅ Feature 1: Designed for {keyword} lovers",
            f"✅ Feature 2: High durability and quality",
            f"✅ Feature 3: Easy to use and maintain"
        ]

        # Generate summary
        summary = f"This {keyword} is perfect for anyone looking for quality and performance. Ideal for daily use and guaranteed satisfaction."

        # Display results
        st.subheader("Sample Titles")
        for t in titles:
            st.write(t)

        st.subheader("Sample Bullet Points")
        for b in bullets:
            st.write(b)

        st.subheader("Sample Product Summary")
        st.write(summary)

        # Mark demo as used
        st.session_state.demo_used = True

        # Show hire message
        st.success(
            "Liked the sample? I can generate full optimized listings with multiple titles, bullets, and summaries ready to post on Amazon. Hire me now!"
        )

    else:
        st.warning(
            "You have reached the free demo limit. Hire me to generate full professional listings."
        )
