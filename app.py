import streamlit as st
import requests
import re
from datetime import datetime

st.set_page_config(page_title="AskMyVideo", page_icon="🎥", layout="centered")

# --- Custom CSS to fix cursor on disabled button ---
st.markdown(
    """
    <style>
    button[disabled], button[disabled]:hover, button[disabled]:focus {
        cursor: pointer !important;
        opacity: 0.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
def init_session():
    st.session_state.setdefault("transcript", None)
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("loading_transcript", False)
    st.session_state.setdefault("loading_answer", False)

init_session()

def validate_youtube_url(url):
    return bool(re.search(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url))


# --- Sidebar: YouTube Video Input ---
with st.sidebar:
    st.header("📹 Load YouTube Video")
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

    languages = {
        "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
        "Italian": "it", "Portuguese": "pt", "Russian": "ru", 
        "Japanese": "ja", "Korean": "ko", "Chinese": "zh"
    }
    selected_language = st.selectbox("Transcript Language", list(languages.keys()))
    lang_code = languages[selected_language]

    api_url = "http://localhost:8010"
    valid_url = validate_youtube_url(youtube_url)

    if youtube_url and not valid_url:
        st.error("❌ Invalid YouTube URL")

    if st.button("🔄 Extract Transcript", disabled=not valid_url):
        st.session_state.loading_transcript = True
        try:
            with st.spinner("Extracting transcript..."):
                res = requests.post(
                    f"{api_url}/extract-id",
                    json={"url": youtube_url, "language_code": lang_code},
                    timeout=60
                )
                if res.status_code == 200:
                    data = res.json()
                    transcript = data.get("transcript", "")
                    if transcript:
                        st.session_state.transcript = transcript
                        st.session_state.chat_history = []
                        st.success("✅ Transcript extracted!")
                        st.rerun()
                    else:
                        st.error("❌ No transcript found.")
                else:
                    st.error(f"❌ Server error: {res.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        st.session_state.loading_transcript = False


# --- Main Chat Interface ---
st.title("🎥 AskMyVideo")
st.caption("Chat with YouTube videos using AI")

if st.session_state.transcript:
    with st.expander("📄 View Transcript"):
        st.code(st.session_state.transcript[:5000], language="text")

    st.divider()

    # --- Display Chat History ---
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["message"])

    # --- Input Box ---
    user_input = st.chat_input("Ask something about the video...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{api_url}/rag-qa",
                    json={
                        "transcript": st.session_state.transcript[:5000],
                        "question": user_input
                    },
                    timeout=45
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "🤖 No answer found.")
                else:
                    answer = f"❌ Server Error {response.status_code}: {response.text}"
        except Exception as e:
            answer = f"❌ Request failed: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "message": answer})
        st.rerun()
else:
    st.info("📌 Enter a valid YouTube URL in the sidebar, extract the transcript, and start chatting!")
