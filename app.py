import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Amazon Product Research AI", page_icon="🛍️")

# ---------- API KEYS ----------
gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# ---------- CONFIGURE APIs ----------
if gemini_key:
    genai.configure(api_key=gemini_key)

if openai_key:
    client = OpenAI(api_key=openai_key)

# ---------- HEADER ----------
st.title("🛍️ Amazon Product Research AI Assistant")
st.write("Find profitable Amazon products, generate titles, and bullet points instantly.")

st.info("🚀 This AI tool helps Amazon sellers find winning products and create listings in seconds.")

st.markdown("### 💡 Try these:")
st.markdown("- Suggest a profitable Amazon product")
st.markdown("- Give product idea in kitchen niche")
st.markdown("- Create listing for water bottle")

# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- TEXT GENERATION FUNCTION ----------
def generate_text(user_input):
    if not openai_key:
        return "⚠️ OpenAI API key missing."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an Amazon product research expert."},
                {"role": "user", "content": f"""
User query: {user_input}

Respond in this format:

Product Idea:
(Write a unique and profitable product idea)

Titles:
1. Title 1
2. Title 2

Bullet Points:
- Point 1
- Point 2
- Point 3

Why this product?
(Short explanation why it can sell well)
"""}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
# ---------- CHAT INPUT ----------
user_input = st.chat_input("Ask about Amazon products...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Generating..."):
        reply = generate_text(user_input)

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- CLEAR CHAT ----------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
