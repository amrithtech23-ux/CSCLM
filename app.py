import streamlit as st
import requests
import json
import random
import re
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="⚖️ Cloud Computing Chatbot",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with updated suggestion card styling
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[data-testid="baseButton-header"] {visibility: hidden;}
    
    /* Main Title */
    .main-title {
        color: #1e293b !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin: 20px 0 10px 0 !important;
        padding: 25px !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        display: block !important;
    }
    
    /* Info Boxes */
    .info-bar {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #475569;
        font-size: 1.05rem;
    }
    
    .knowledge-bar {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #1e3a8a;
        font-size: 1.05rem;
    }

    /* Section Headers */
    .section-header {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 30px 0 20px 0;
        text-align: center;
    }

    /* Input Area */
    .stTextArea textarea {
        background-color: #f8fafc;
        color: #334155;
        font-weight: 600;
        font-size: 1.1rem;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 15px;
    }
    
    /* Result Area - ULTRA COMPACT SPACING */
    .result-area {
        background-color: #f8fafc;
        color: #334155;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.25;
        margin-top: 20px;
        white-space: pre-wrap;
    }
    
    /* Remove ALL extra margin between paragraphs */
    .result-area p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.25 !important;
    }
    
    .result-area p + p {
        margin-top: 0.4em !important;
    }
    
    .result-area h1, .result-area h2, .result-area h3, .result-area h4 {
        margin: 0.5em 0 0.3em 0 !important;
        line-height: 1.25 !important;
    }
    
    .result-area ul, .result-area ol {
        margin: 0.2em 0 !important;
        padding-left: 1.5em;
    }
    
    .result-area li {
        margin: 0.1em 0 !important;
        line-height: 1.25 !important;
    }
    
    .result-area br {
        line-height: 0.5 !important;
    }
    
    /* Suggestion Cards - BLACK BORDER, WHITE BACKGROUND, BLUE TEXT */
    .suggestion-card {
        background-color: #ffffff !important;
        color: #2563eb !important;  /* Blue color */
        font-size: 1rem;
        font-weight: 600;
        padding: 15px 20px;
        margin: 8px 0;
        border-radius: 8px;
        border: 2px solid #000000 !important;  /* Black border */
        text-align: left;
        width: 100%;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
    }
    
    .suggestion-card:hover {
        background-color: #f0f9ff !important;  /* Light blue on hover */
        border-color: #2563eb !important;  /* Blue border on hover */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.2);
    }
    
    .suggestion-card:active {
        transform: translateY(0);
    }
    
    /* Use button styling */
    .use-btn {
        background-color: #f8fafc;
        color: #475569;
        border: 1px solid #cbd5e1;
        padding: 5px 12px;
        border-radius: 5px;
        font-size: 0.85rem;
        cursor: pointer;
        margin-top: 5px;
    }
    
    .use-btn:hover {
        background-color: #e2e8f0;
        border-color: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load topics and remove duplicates
@st.cache_data
def load_knowledge_base():
    """Load cloud computing topics from the knowledge base file and remove duplicates."""
    kb_path = Path("knowledge_base/cloud_computing_topics.txt")
    topics = []
    
    if kb_path.exists():
        with open(kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'^\d+\.\s+(.+)$', content, re.MULTILINE)
            unique_topics = list(set(match.strip() for match in matches if match.strip()))
            unique_topics.sort()
            return unique_topics
    else:
        return []

# Initialize session state
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

# Load knowledge base
all_topics = load_knowledge_base()

# Initialize suggestions if empty
if not st.session_state.suggestions and all_topics:
    st.session_state.suggestions = random.sample(all_topics, min(10, len(all_topics)))

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    try:
        from streamlit import secrets
        if "OPENROUTER_API_KEY" in secrets:
            st.session_state.api_key = secrets["OPENROUTER_API_KEY"]
            st.success("✅ API Key loaded from secrets!")
    except:
        pass
    
    if not st.session_state.api_key:
        key = st.text_input("OpenRouter API Key", type="password")
        if key:
            st.session_state.api_key = key
            st.success("✅ API Key saved!")
    
    st.markdown("---")
    st.info(f"📚 **Loaded {len(all_topics)} unique topics**")

# --- UI Layout ---

# 1. Title Section
st.markdown('<div class="main-title">⚖️ Cloud Computing Chatbot</div>', unsafe_allow_html=True)

# 2. Info Bars
st.markdown('<div class="info-bar">🎯 <strong>Target Audience:</strong> B.E. CS / B.Tech IT Engineering Students & IT Industry Job Seekers</div>', unsafe_allow_html=True)
st.markdown(f'<div class="knowledge-bar">📚 <strong>Knowledge Base:</strong> Loaded with 1500++ unique comprehensive Cloud Computing topics</div>', unsafe_allow_html=True)

# 3. Input Section
st.markdown('<div class="section-header">📝 Enter Your Query</div>', unsafe_allow_html=True)

user_query = st.text_area(
    "",
    value=st.session_state.query,
    height=120,
    placeholder="Ask about cloud computing concepts...",
    key="user_query_input",
    label_visibility="collapsed"
)

col_btn1, col_btn2 = st.columns([2, 1])
with col_btn1:
    submit_btn = st.button("📤 Submit Prompt", use_container_width=True)
with col_btn2:
    reset_btn = st.button("🔄 Reset", use_container_width=True)

# 4. Logic for Submit & Result Display
if submit_btn and user_query:
    if not st.session_state.api_key:
        st.error("❌ Please configure your OpenRouter API Key in the sidebar.")
    else:
        with st.spinner("🤖 Getting response from Qwen AI..."):
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/amrithtech23-ux/CSCLM",
                    "X-Title": "CSCLM Cloud Computing Chatbot"
                }
                
                system_prompt = f"""You are an expert Cloud Computing instructor for B.E. Computer Science and B.Tech IT students.
                Your knowledge base contains {len(all_topics)} unique topics covering distributed systems, virtualization, security, and programming models.
                
IMPORTANT INSTRUCTIONS:
- Provide clear, detailed, educational answers with practical examples
- DO NOT use introductory phrases like "Certainly!", "Of course!", "Sure!", "I'd be happy to help", etc.
- Start directly with the answer content
- Use concise paragraphs with minimal spacing - keep paragraphs tight
- Structure information with headings and bullet points where appropriate
- Focus on technical accuracy and educational value"""
                
                payload = {
                    "model": "qwen/qwen-2.5-72b-instruct",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result_text = response.json()["choices"][0]["message"]["content"]
                    result_text = re.sub(r'^(Certainly!|Of course!|Sure!|I\'d be happy to help|Absolutely!)\s*', '', result_text, flags=re.IGNORECASE)
                    st.session_state.result = result_text.strip()
                    st.success("✅ Response received!")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display Result if exists
if st.session_state.result:
    st.markdown('<div class="section-header">📚 Response</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="result-area">
        {st.session_state.result}
        </div>
    """, unsafe_allow_html=True)

# 5. Suggestions Section (COPYABLE - BELOW RESULT)
st.markdown('<div class="section-header">💡 System Suggestion Prompts</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.95rem; margin-bottom: 20px;">💡 Click to use • Text is selectable for copying</p>', unsafe_allow_html=True)

# Create a grid of copyable suggestion cards (2 columns)
for i in range(0, len(st.session_state.suggestions), 2):
    cols = st.columns(2)
    
    # First suggestion - Copyable card with black border, white background, blue text
    if i < len(st.session_state.suggestions):
        suggestion_1 = st.session_state.suggestions[i]
        with cols[0]:
            st.markdown(f"""
                <div class="suggestion-card" data-query="{suggestion_1}">
                • {suggestion_1}
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📋 Use", key=f"use_{i}", help="Use this prompt"):
                st.session_state.query = suggestion_1
                st.rerun()
            
    # Second suggestion - Copyable card with black border, white background, blue text
    if i + 1 < len(st.session_state.suggestions):
        suggestion_2 = st.session_state.suggestions[i+1]
        with cols[1]:
            st.markdown(f"""
                <div class="suggestion-card" data-query="{suggestion_2}">
                • {suggestion_2}
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📋 Use", key=f"use_{i+1}", help="Use this prompt"):
                st.session_state.query = suggestion_2
                st.rerun()

# Refresh button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Refresh Suggestions", use_container_width=True):
    if all_topics:
        st.session_state.suggestions = random.sample(all_topics, min(10, len(all_topics)))
        st.rerun()

# Reset Logic
if reset_btn:
    st.session_state.query = ""
    st.session_state.result = ""
    if all_topics:
        st.session_state.suggestions = random.sample(all_topics, min(10, len(all_topics)))
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                text-align: center; color: #4b5563; font-weight: bold; 
                padding: 25px; margin-top: 30px; border-radius: 10px;">
        <p style="font-size: 1.3rem; margin-bottom: 8px;">🎓 CSCLM - Cloud Computing Learning Module</p>
        <p style="font-size: 1.05rem; margin-bottom: 12px;">B.E. Computer Science | B.Tech Information Technology</p>
        <p style="font-size: 0.95rem; color: #6b7280;">License: MIT | Powered by OpenRouter API & Qwen AI</p>
    </div>
""", unsafe_allow_html=True)
