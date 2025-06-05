import streamlit as st
import time
from datetime import datetime

from modules.transcript import get_transcript_from_youtube
from modules.rag_pipeline import setup_qa_chain, answer_question

# Page config with better theme
st.set_page_config(
    page_title="AskMyVideo - AI Video Chat", 
    layout="wide", 
    page_icon="🎥",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Card styling */
    .stCard {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Chat message styling - FIXED COLOR CONTRAST */
    .chat-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #1976d2;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        color: #333333; /* Added explicit text color for contrast */
    }
    
    .chat-response {
        background: #f1f8e9;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #388e3c;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #c3e6cb;
        color: #333333; /* Added explicit text color for contrast */
    }
    
    /* Status styling */
    .status-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .status-error {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Stats styling */
    .stats-container {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
<div class="main-header">
    <h1>🎥 AskMyVideo</h1>
    <p>Transform any YouTube video into an interactive AI conversation</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for video loading and stats
with st.sidebar:
    st.header("🎬 Video Management")        # Video loading form
    with st.form("video_form", clear_on_submit=False):
        st.subheader("📹 Load YouTube Video")
        video_url = st.text_input(
            "YouTube URL", 
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            help="Paste any YouTube video URL here"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🚀 Process Video", use_container_width=True)
        with col2:
            if st.form_submit_button("🗑️ Clear", use_container_width=True):
                st.session_state.transcript = None
                st.session_state.qa_chain = None
                st.session_state.chat_history = []
                st.session_state.video_loaded = False
                st.rerun()
    
    # Processing status
    if submitted and video_url and not st.session_state.processing:
        st.session_state.processing = True
        
        with st.status("🔄 Processing video...", expanded=True) as status:
            st.write("🎯 Extracting transcript...")
            transcript, message = get_transcript_from_youtube(video_url)
            
            if transcript:
                st.session_state.transcript = transcript
                st.write("🤖 Setting up AI system...")
                
                qa_chain, error = setup_qa_chain(transcript)
                
                if qa_chain:
                    st.session_state.qa_chain = qa_chain
                    st.session_state.video_loaded = True
                    status.update(label="✅ Ready to chat!", state="complete", expanded=False)
                    st.success("🎉 Video processed successfully!")
                else:
                    status.update(label=f"❌ Setup Error: {error}", state="error")
                    st.error(f"Failed to setup Q&A system: {error}")
            else:
                status.update(label=f"❌ {message}", state="error")
                st.error(f"Failed to extract transcript: {message}")
        
        st.session_state.processing = False
    
    # Video statistics
    if st.session_state.video_loaded:
        st.markdown("---")
        st.subheader("📊 Session Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions Asked", len(st.session_state.chat_history))
        with col2:
            st.metric("Transcript Length", f"{len(st.session_state.transcript):,} chars")
        
        # Transcript preview
        with st.expander("📄 View Transcript"):
            st.text_area(
                "Video Transcript", 
                st.session_state.transcript[:2000] + "..." if len(st.session_state.transcript) > 2000 else st.session_state.transcript,
                height=200, 
                disabled=True
            )

# Main content area
if st.session_state.video_loaded:
    # Question input section
    st.subheader("🤔 Ask Your Questions")
    
    col1, col2, col3 = st.columns([6, 2, 2])
    with col1:
        question = st.text_input(
            "What would you like to know about this video?",
            placeholder="e.g., What are the main points discussed?",
            label_visibility="collapsed"
        )
    with col2:
        ask_button = st.button("💬 Ask", use_container_width=True, type="primary")
    with col3:
        if st.session_state.chat_history:
            clear_chat = st.button("🗑️ Clear Chat", use_container_width=True)
    
    # Quick questions suggestions
    if not st.session_state.chat_history:
        st.markdown("**💡 Try these questions:**")
        quick_questions = [
            "What are the main topics covered?",
            "Can you summarize the key points?",
            "What examples are mentioned?",
            "What conclusions are drawn?"
        ]
        
        cols = st.columns(len(quick_questions))
        for i, q in enumerate(quick_questions):
            with cols[i]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    question = q
                    ask_button = True
    
    # Process question
    if ask_button and question:
        with st.spinner("🧠 Analyzing your question..."):
            try:
                start = time.time()
                answer = answer_question(st.session_state.qa_chain, question)
                end = time.time()
                
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "response_time": f"{end - start:.2f}s",
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
    
    # Clear chat functionality
    if st.session_state.chat_history and 'clear_chat' in locals() and clear_chat:
        st.session_state.chat_history = []
        st.rerun()
    
    # Chat display
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💭 Conversation History")
        
        # Export option
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            if len(st.session_state.chat_history) > 0:
                chat_export = "\n\n".join([
                    f"🙋 Q: {chat['question']}\n🤖 A: {chat['answer']}\n⏰ {chat['timestamp']} ({chat['response_time']})"
                    for chat in st.session_state.chat_history
                ])
                st.download_button(
                    label="📥 Export Conversation",
                    data=chat_export,
                    file_name=f"video_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
        
        # Display chat messages - FIXED COLOR CONTRAST IN MARKDOWN
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                # Question
                st.markdown(f"""
                <div class="chat-message">
                    <strong>🙋 You asked:</strong><br>
                    {chat['question']}
                </div>
                """, unsafe_allow_html=True)
                
                # Answer with improved styling
                st.markdown(f"""
                <div class="chat-response">
                    <strong>🤖 AI Response:</strong><br>
                    {chat['answer']}
                    <br><br>
                    <small style="color: #333333;">
                        🕒 {chat['timestamp']} • ⚡ {chat['response_time']}
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                if i < len(st.session_state.chat_history) - 1:
                    st.markdown("---")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
        <h2>🚀 Get Started</h2>
        <p style="font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem;">
            Upload a YouTube video in the sidebar to begin your AI-powered conversation!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step-by-step guide using Streamlit columns
    st.markdown("### How it works:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; height: 150px;">
            <h3 style="color: #667eea;">🎯 Step 1</h3>
            <p style="color: #6c757d;">Paste your YouTube URL in the sidebar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; height: 150px;">
            <h3 style="color: #667eea;">🤖 Step 2</h3>
            <p style="color: #6c757d;">AI extracts and processes the video content</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; height: 150px;">
            <h3 style="color: #667eea;">💬 Step 3</h3>
            <p style="color: #6c757d;">Start chatting and ask any questions!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Smart Analysis
        AI understands context and provides accurate answers about your video content.
        """)
    with col2:
        st.markdown("""
        ### 🎯 Auto-Caption
        Automatic transcript extraction from YouTube videos.
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Export Results
        Save your conversations and insights for later reference.
        """)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #6c757d; font-size: 0.9rem; padding: 1rem;">
    <strong>AskMyVideo</strong> • Powered by AI • Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)