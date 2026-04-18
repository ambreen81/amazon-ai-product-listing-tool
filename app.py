import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Amazon AI Chatbot", page_icon="🛍️")

# ---------- API KEYS ----------
gemini_key = st.secrets.get("GEMINI_API_KEY", None)
openai_key = st.secrets.get("OPENAI_API_KEY", None)

# ---------- CONFIGURE APIs ----------
if gemini_key:
    genai.configure(api_key=gemini_key)

if openai_key:
    client = OpenAI(api_key=openai_key)

# ---------- HEADER ----------
st.title("🛍️ Amazon AI Chatbot Assistant")

# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- TEXT GENERATION FUNCTION ----------
def generate_text(user_input):
    if not gemini_key:
        return "⚠️ Gemini API key missing."

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""
You are an Amazon product research expert.

User query: {user_input}

Respond in this format:

**Product Idea:**
(Write a unique and profitable product idea)

**Titles:**
1. Title 1
2. Title 2

**Bullet Points:**
- Point 1
- Point 2
- Point 3

**Why this product?**
(Short explanation why it can sell well)
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {e}"

# ---------- CHAT INPUT ----------
user_input = st.chat_input("Ask about Amazon products...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    reply = generate_text(user_input)

    # Show response
    with st.chat_message("assistant"):
        st.write(reply)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- CLEAR CHAT ----------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
