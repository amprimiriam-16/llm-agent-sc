"""
Streamlit Frontend Application
SCIP Question-Answering Platform
"""
import streamlit as st
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from frontend.components.chat import render_chat_interface
from frontend.components.upload import render_upload_interface
from frontend.components.analytics import render_analytics
from frontend.utils.api_client import APIClient
from backend.core.config import settings


# Page configuration
st.set_page_config(
    page_title="SCIP Question-Answering Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .source-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .basf-logo {
        color: #000000;
        font-weight: bold;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient()
    if "use_agentic" not in st.session_state:
        st.session_state.use_agentic = True


def render_sidebar():
    """Render sidebar with settings and info"""
    with st.sidebar:
        st.markdown('<p class="basf-logo">BASF SCIP</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Settings
        st.subheader("⚙️ Settings")
        
        st.session_state.use_agentic = st.toggle(
            "Use Agentic RAG",
            value=st.session_state.use_agentic,
            help="Enable intelligent multi-step reasoning"
        )
        
        max_sources = st.slider(
            "Max Sources",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of source documents to retrieve"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Response creativity (0=focused, 1=creative)"
        )
        
        st.markdown("---")
        
        # Mode selection
        mode = st.radio(
            "Mode",
            options=["💬 Chat", "📤 Upload Documents", "📊 Analytics"],
            index=0
        )
        
        st.markdown("---")
        
        # Info
        st.subheader("ℹ️ About")
        st.info(
            """
            **SCIP QA Platform**
            
            Enterprise AI-powered question-answering system for BASF's Supply Chain Intelligence Platform.
            
            **Features:**
            - Agentic RAG with reasoning
            - Vector semantic search
            - Azure OpenAI integration
            - MCP protocol support
            
            **Classification:** CONFIDENTIAL
            """
        )
        
        # Health check
        if st.button("🏥 Check System Health"):
            with st.spinner("Checking..."):
                health = st.session_state.api_client.get_health()
                if health.get("status") == "healthy":
                    st.success("✅ System Healthy")
                else:
                    st.error("❌ System Issues Detected")
        
        return mode, max_sources, temperature


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">🔍 SCIP Question-Answering Platform</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">AI-powered insights from BASF Supply Chain Intelligence</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    mode, max_sources, temperature = render_sidebar()
    
    # Main content based on mode
    if mode == "💬 Chat":
        render_chat_interface(
            api_client=st.session_state.api_client,
            use_agentic=st.session_state.use_agentic,
            max_sources=max_sources,
            temperature=temperature
        )
    elif mode == "📤 Upload Documents":
        render_upload_interface(st.session_state.api_client)
    else:  # Analytics
        render_analytics(st.session_state.api_client)


if __name__ == "__main__":
    main()
