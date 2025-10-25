import streamlit as st
import google.generativeai as genai
import io
from datetime import datetime

# --------------------------------------------------------
# CONFIG
# --------------------------------------------------------
st.set_page_config(
    page_title="Amazon AI Product Research Tool",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------------
# Helper: set CSS for premium bright cards
# ------------------------
CARD_STYLE = """
border-radius: 12px;
padding: 16px;
box-shadow: 0 6px 18px rgba(18, 38, 63, 0.08);
background: white;
"""

HEADER_STYLE = """
background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
padding: 18px;
border-radius: 12px;
color: white;
"""

# --------------------------------------------------------
# Gemini connection (try latest then fallback)
# --------------------------------------------------------
def initialize_gemini():
    """Configure genai and return active model string or raise exception."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini API key not found. Add it to .streamlit/secrets.toml")

    genai.configure(api_key=api_key)

    # Try newest model first, fallback to stable older model
    for model_name in ["models/gemini-2.0-flash-exp", "models/gemini-1.5-flash"]:
        try:
            test_model = genai.GenerativeModel(model_name)
            # quick lightweight test call
            test_model.generate_content("Hello")
            return model_name
        except Exception:
            continue

    # If we exited loop, none worked
    raise RuntimeError("Unable to connect to Gemini with available models.")


# Try initialize and show status on top of the app
try:
    ACTIVE_MODEL = initialize_gemini()
    st.session_state["gemini_status"] = f"Connected ({ACTIVE_MODEL})"
except Exception as e:
    st.session_state["gemini_status"] = f"Error: {e}"
    # Show big red banner and stop further execution
    st.markdown(
        f"""
        <div style="
            background-color: #ffebe8;
            color: #7f1d1d;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
        ">
            ❌ Gemini Connection Issue — {e}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# --------------------------------------------------------
# SIDEBAR (Brand + Info)
# --------------------------------------------------------
with st.sidebar:
    st.markdown("## 🤖 Amazon AI Tools")
    st.markdown("**Developed by Ambreen**")
    st.markdown("---")
    st.markdown("**Tool:** Amazon AI Product Research")
    st.markdown("**Features:** AI product summary, titles, bullets, description, download")
    st.markdown("---")
    st.markdown(f"**API Status:** {st.session_state['gemini_status']}")
    st.markdown("**Tip:** Use keywords (e.g., `wireless mouse`, `yoga mat`) for best results.")
    st.markdown("---")
    st.markdown("Need custom features? Contact me on Fiverr for a tailored Streamlit AI tool!")

# --------------------------------------------------------
# MAIN HEADER (Premium Bright)
# --------------------------------------------------------
st.markdown(f"<div style='{HEADER_STYLE}'><h2 style='margin:0'>🤖 Amazon AI Product Research Tool</h2><div style='opacity:0.95'>Generate optimized titles, bullets & descriptions</div></div>", unsafe_allow_html=True)
st.write("")  # spacing

# --------------------------------------------------------
# INPUT AREA
# --------------------------------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    keyword = st.text_input("🔍 Enter product keyword (e.g., wireless mouse):", placeholder="Type a product keyword here")
with col2:
    if st.button("Try Sample"):
        # fill sample keyword when user clicks sample
        st.experimental_set_query_params(sample="true")
        keyword = "wireless mouse"
        st.experimental_rerun()

st.caption("Pro tip: use short keywords or one-line product descriptions for best outputs.")

# --------------------------------------------------------
# Generate Button
# --------------------------------------------------------
if st.button("Generate Insights"):
    if not keyword or keyword.strip() == "":
        st.warning("⚠️ Please enter a product keyword first.")
    else:
        with st.spinner("Analyzing product and generating insights... ⏳"):
            # Build a clear, structured prompt
            prompt = f"""
You are an expert Amazon listing optimizer. Provide well-structured Amazon product insights for the product keyword: '{keyword}'.

Return the result with clearly labeled sections:
SUMMARY:
- A short product summary (1-2 sentences).

TITLES:
- Two SEO-friendly title ideas (each on a new line).

BULLETS:
- Three key bullet points (each bullet on a separate line).

DESCRIPTION:
- One short, engaging product description (2-3 sentences).

Use simple headings (SUMMARY, TITLES, BULLETS, DESCRIPTION) and bullet formatting for clarity.
            """

            try:
                model = genai.GenerativeModel(ACTIVE_MODEL)
                response = model.generate_content(prompt)

                # Some responses return a .text attribute; fallback to str(response) if not present
                generated_text = getattr(response, "text", None) or str(response)

                # Show results in premium cards
                st.markdown("<div style='display:flex;gap:16px;flex-direction:column'>", unsafe_allow_html=True)

                # We will display the full AI output first, then split sections if possible
                st.markdown(f"<div style='{CARD_STYLE}'>", unsafe_allow_html=True)
                st.markdown("### 🔎 Full AI Output")
                st.code(generated_text)
                st.markdown("</div>", unsafe_allow_html=True)

                # Try to split by headings: SUMMARY, TITLES, BULLETS, DESCRIPTION
                # This is a forgiving split — if headings exist, we extract; else show full output below
                lower = generated_text.lower()
                def extract_section(text, start_token, end_tokens):
                    start = text.find(start_token)
                    if start == -1:
                        return None
                    # find earliest next token among end_tokens
                    next_indices = [text.find(t, start + len(start_token)) for t in end_tokens if text.find(t, start + len(start_token)) != -1]
                    if next_indices:
                        end = min(next_indices)
                        return text[start + len(start_token):end].strip()
                    else:
                        return text[start + len(start_token):].strip()

                summary = extract_section(lower, "summary", ["titles", "title", "bullets", "description"])
                titles = extract_section(lower, "titles", ["bullets", "description", "summary"])
                bullets = extract_section(lower, "bullets", ["description", "titles", "summary"])
                description = extract_section(lower, "description", ["summary", "titles", "bullets"])

                # display parsed sections in separate cards if found
                if summary:
                    st.markdown(f"<div style='{CARD_STYLE}'>", unsafe_allow_html=True)
                    st.markdown("### 📝 Summary")
                    st.write(summary)
                    st.markdown("</div>", unsafe_allow_html=True)

                if titles:
                    st.markdown(f"<div style='{CARD_STYLE}'>", unsafe_allow_html=True)
                    st.markdown("### 🏷️ Title Ideas")
                    st.write(titles)
                    st.markdown("</div>", unsafe_allow_html=True)

                if bullets:
                    st.markdown(f"<div style='{CARD_STYLE}'>", unsafe_allow_html=True)
                    st.markdown("### • Key Bullet Points")
                    st.write(bullets)
                    st.markdown("</div>", unsafe_allow_html=True)

                if description:
                    st.markdown(f"<div style='{CARD_STYLE}'>", unsafe_allow_html=True)
                    st.markdown("### 🧾 Product Description")
                    st.write(description)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Prepare text file for download: include full generated output and a header
                now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                filename = f"{keyword.replace(' ', '_')}_amazon_insights_{now}.txt"
                txt_content = f"Keyword: {keyword}\nGenerated: {datetime.utcnow().isoformat()}Z\n\n{generated_text}"

                # Download button
                st.download_button(
                    label="⬇️ Download Results as .txt",
                    data=txt_content,
                    file_name=filename,
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"⚠️ An error occurred while generating content: {e}")
                st.info("Tip: If this happens often, check your Gemini API quota or try again later.")

# --------------------------------------------------------
# Footer / Small note
# --------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #444; font-size: 15px; margin-top: 30px;'>
        Built with ❤️ using <b>Gemini</b> • 
        <a href='https://www.fiverr.com/Ambreen Asad' target='_blank' style='color: #16a34a; text-decoration: none; font-weight: 600;'>
            Message me on Fiverr
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


