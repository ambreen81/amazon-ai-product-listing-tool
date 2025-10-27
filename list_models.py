import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Configure Gemini API
genai.configure(api_key=api_key)

print("\n🔍 Fetching available Gemini models...\n")

# List all available models
models = genai.list_models()

for m in models:
    print(f"Model name: {m.name}")
    if "generateContent" in m.supported_generation_methods:
        print("✅ Supports generateContent")
    else:
        print("❌ Does not support generateContent")
    print("-" * 60)

print("\n✅ Done! You can now copy the correct model name into your Streamlit app.")
