import streamlit as st
from transformers import pipeline

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Multilingual Translator", page_icon="🌍", layout="centered")

# -------------------------
# Custom UI
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5f0e8;
    color: #1a1a2e;
}
.stApp { background: #f5f0e8; }
#MainMenu, footer, header { visibility: hidden; }

.title-wrap {
    text-align: center;
    padding: 36px 0 8px;
}
.title-wrap h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: #1a1a2e;
    letter-spacing: -0.01em;
    margin: 0;
}
.title-wrap .flag { font-size: 1.8rem; }
.subtitle {
    text-align: center;
    font-size: 0.82rem;
    color: #7a6f5e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 32px;
}
.divider {
    border: none;
    border-top: 1.5px solid #d4c9b0;
    margin: 0 0 28px;
}
.card {
    background: #fffdf7;
    border: 1.5px solid #d4c9b0;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 20px;
}
.card-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #9e8f75;
    margin-bottom: 10px;
}
.result-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #1a1a2e;
    line-height: 1.5;
    min-height: 40px;
}
.stTextArea textarea {
    background: #fffdf7 !important;
    border: 1.5px solid #d4c9b0 !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 14px 16px !important;
}
.stTextArea textarea:focus {
    border-color: #c0a87a !important;
    box-shadow: 0 0 0 3px rgba(192,168,122,0.15) !important;
}
.stButton > button {
    background: #1a1a2e !important;
    color: #f5f0e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2e2e4a !important;
    transform: translateY(-1px) !important;
}
.history-item {
    background: #fffdf7;
    border: 1px solid #e8e0cc;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    font-size: 0.88rem;
}
.history-en { color: #7a6f5e; margin-bottom: 4px; font-size: 0.78rem; letter-spacing: 0.05em; }
.history-fr { color: #1a1a2e; font-family: 'Playfair Display', serif; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load model (same as original)
# -------------------------
@st.cache_resource
def load_models():
    return {
        "English → French": pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr"),
        "French → English": pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en"),
        "English → Hindi": pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi"),
        "Hindi → English": pipeline("translation_hi_to_en", model="Helsinki-NLP/opus-mt-hi-en"),
        "English → German": pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de"),
        "German → English": pipeline("translation_de_to_en", model="Helsinki-NLP/opus-mt-de-en"),
        "English → Chinese": pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh"),
        "Chinese → English": pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en"),
    }

with st.spinner("Loading models..."):
    models = load_models()

# -------------------------
# Translate function
# -------------------------
def translate_text(user_input, model_name):
    translator = models[model_name]
    result = translator(user_input, max_length=400)
    return result[0]["translation_text"]

# -------------------------
# Session state
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "translation" not in st.session_state:
    st.session_state.translation = ""

# -------------------------
# UI
# -------------------------
st.title("🌍 Multilingual Translator")

# ✅ NEW: Language selection dropdown
language_choice = st.selectbox(
    "Select Translation",
    list(models.keys())
)

user_input = st.text_area("Enter text:", height=130)

if st.button("TRANSLATE"):
    if user_input.strip():
        with st.spinner("Translating..."):
            output = translate_text(user_input.strip(), language_choice)
            st.session_state.translation = output
            st.session_state.history.insert(0, {
                "input": user_input.strip(),
                "output": output,
                "lang": language_choice
            })
    else:
        st.warning("Please enter some text.")

# -------------------------
# Output
# -------------------------
if st.session_state.translation:
    st.subheader("Translated Text")
    st.write(st.session_state.translation)

# -------------------------
# History
# -------------------------
if st.session_state.history:
    st.subheader("Recent Translations")
    for item in st.session_state.history[:5]:
        st.write(f"**{item['lang']}**")
        st.write(f"Input: {item['input']}")
        st.write(f"Output: {item['output']}")
        st.write("---")