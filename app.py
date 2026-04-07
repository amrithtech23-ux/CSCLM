import streamlit as st
import requests
import json
import random
import os

# Page configuration - hide sidebar by default
st.set_page_config(
    page_title="⚖️ CLOUD COMPUTING Chatbot",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling and hiding elements
st.markdown("""
    <style>
    /* Hide the main menu */
    #MainMenu {visibility: hidden;}
    
    /* Hide footer */
    footer {visibility: hidden;}
    
    /* Hide sidebar toggle button */
    button[data-testid="baseButton-header"] {visibility: hidden;}
    
    /* Main title styling - Gray background, White text, Larger font */
    .main-title {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        padding: 30px 40px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        letter-spacing: 0.5px;
    }
    
    /* Suggestion prompt styling - Mild color background, Bold, Bigger */
    .suggestion-button {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        color: #374151;
        font-size: 1.15rem;
        font-weight: bold;
        padding: 18px 24px;
        margin: 10px 0;
        border-radius: 10px;
        border: 2px solid #d1d5db;
        text-align: left;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .suggestion-button:hover {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        border-color: #6b7280;
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Input text area styling */
    .stTextArea textarea {
        background-color: #ffffff;
        color: #1f2937;
        font-weight: 600;
        font-size: 1.1rem;
        border: 2px solid #9ca3af;
        border-radius: 8px;
    }
    
    /* Result text area styling */
    .result-area {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #6b7280;
        font-weight: 600;
        font-size: 1.1rem;
        min-height: 300px;
        white-space: pre-wrap;
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #6b7280;
        padding: 12px 30px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
        border-color: #374151;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Section headers */
    .section-header {
        color: #4b5563;
        font-size: 1.6rem;
        font-weight: bold;
        margin: 25px 0 15px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #9ca3af;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-left: 5px solid #6b7280;
        padding: 18px;
        margin: 20px 0;
        border-radius: 8px;
        color: #374151;
        font-size: 1.05rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Academic theme - overall container */
    .main-container {
        background-color: #fafafa;
        padding: 20px;
        border-radius: 12px;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# topics from knowledge base
cloud_topics = [
    "Evolution from centralized to distributed systems: A technical timeline",
    "Client-server vs. peer-to-peer architecture: A comparative study",
    "Clustered computing: Types (high availability, load balancing, HPC)",
    "Grid computing fundamentals and its differences from cloud",
    "Utility computing: Pay-per-use model origins",
    "Virtualization as the core enabler of network-based systems",
    "Service-oriented architecture (SOA) in cloud environments",
    "Web services (REST, SOAP, WSDL, UDDI) for cloud interoperability",
    "Containerization (Docker) vs. virtual machines: Performance trade-offs",
    "Microservices architecture: Decomposing monolithic apps",
    "Serverless computing (FaaS): Event-driven network-based systems",
    "Software-defined networking (SDN) for cloud data centers",
    "Network function virtualization (NFV) in telecom clouds",
    "Message queuing systems (RabbitMQ, Kafka) for distributed communication",
    "Remote procedure calls (RPC/gRPC) in cloud-native apps",
    "Representational state transfer (REST) constraints for scalable APIs",
    "Edge computing: Extending network-based systems to the periphery",
    "Fog computing: Middle layer between edge and cloud",
    "Content delivery networks (CDN) as a distributed system",
    "Blockchain as a distributed ledger technology in cloud",
    "Distributed databases (Cassandra, CockroachDB) fundamentals",
    "In-memory data grids (Redis, Hazelcast) for performance",
    "Distributed file systems (Ceph, GlusterFS) basics",
    "Consensus algorithms (Paxos, Raft) in cloud systems",
    "Leader election and distributed coordination (ZooKeeper)",
    "Distributed transactions: Two-phase commit (2PC) vs. Saga pattern",
    "CAP theorem and its implications for cloud design",
    "Fallacies of distributed computing (L. Peter Deutsch)",
    "Case study: Google's Borg and Omega schedulers",
    "Case study: Amazon DynamoDB's distributed architecture"
]

# Initialize session state
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))

# Minimal sidebar for API key (hidden by default but accessible)
with st.sidebar:
    st.header("⚙️ API Configuration")
    
    # Try to load API key from Streamlit secrets
    api_key_loaded = False
    try:
        from streamlit import secrets
        if "OPENROUTER_API_KEY" in secrets:
            st.session_state.api_key = secrets["OPENROUTER_API_KEY"]
            api_key_loaded = True
            st.success("✅ API Key loaded from secrets!")
    except:
        pass
    
    if not api_key_loaded:
        api_key_input = st.text_input(
            "Enter OpenRouter API Key:",
            type="password",
            help="Your API key is encrypted"
        )
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("✅ API Key saved!")
    
    st.markdown("---")
    st.info("🎓 **For:** B.E. CS / B.Tech IT Engineering Students & Job Seekers")

# Main Title - Gray background with white text
st.markdown('<p class="main-title">⚖️ CLOUD COMPUTING  Chatbot</p>', unsafe_allow_html=True)

# Subtitle
st.markdown('<p class="subtitle"><b>Interactive Learning Platform for Cloud Computing Concepts</b></p>', unsafe_allow_html=True)

# Info box
st.markdown("""
    <div class="info-box">
        <strong>📚 How to use:</strong> Click on any suggested prompt below OR type your own question about Cloud Computing, 
        then click "Submit Prompt" to get AI-powered answers from Qwen AI model.
    </div>
""", unsafe_allow_html=True)

# Create two main columns
col_left, col_right = st.columns([1, 1])

# LEFT COLUMN - Suggested Prompts
with col_left:
    st.markdown('<p class="section-header">💡 Suggested Prompts (Click to Use)</p>', unsafe_allow_html=True)
    
    # Display 10 random suggestions with mild color background, bold, bigger font
    for i, suggestion in enumerate(st.session_state.suggestions):
        # Create button with custom styling - mild gray background
        btn_key = f"sugg_{i}"
        if st.button(f"📌 {i+1}. {suggestion}", key=btn_key, use_container_width=True):
            st.session_state.query = suggestion
            st.rerun()
    
    # Refresh suggestions button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Suggestions", use_container_width=True):
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
        st.rerun()

# RIGHT COLUMN - Query Input and Results
with col_right:
    st.markdown('<p class="section-header">💬 Enter Your Query</p>', unsafe_allow_html=True)
    
    # Text Field 1 - User Query Input
    user_query = st.text_area(
        "Type your Cloud Computing question here:",
        value=st.session_state.query,
        height=120,
        placeholder="E.g., Explain virtualization in cloud computing...",
        key="user_query_input",
        label_visibility="collapsed"
    )
    
    # Buttons - Submit and Reset
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        submit_btn = st.button("📤 Submit Prompt", use_container_width=True)
    
    with col_btn2:
        reset_btn = st.button("🔄 Reset", use_container_width=True)
    
    # Handle Reset
    if reset_btn:
        st.session_state.query = ""
        st.session_state.result = ""
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
        st.rerun()
    
    # Handle Submit
    if submit_btn and user_query:
        if not st.session_state.api_key:
            st.error("❌ Please configure your OpenRouter API Key in the sidebar (click ☰ menu).")
        else:
            with st.spinner("🤖 Getting response from Qwen AI..."):
                try:
                    # Prepare API request
                    headers = {
                        "Authorization": f"Bearer {st.session_state.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/amrithtech23-ux/CSCLM",
                        "X-Title": "CSCLM Cloud Computing Chatbot"
                    }
                    
                    system_prompt = """You are an expert Cloud Computing instructor for B.E. Computer Science and B.Tech IT students. 
                    Provide clear, detailed, educational answers with practical examples and real-world applications.
                    Structure your responses for easy understanding."""
                    
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
                        result_data = response.json()
                        st.session_state.result = result_data["choices"][0]["message"]["content"]
                        st.session_state.query = user_query
                        st.success("✅ Response received!")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        st.error(f"Details: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Text Field 2 - Result Display (Multi-line)
    st.markdown('<p class="section-header">📚 Response</p>', unsafe_allow_html=True)
    
    if st.session_state.result:
        st.markdown(f"""
            <div class="result-area">
            {st.session_state.result}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="result-area" style="color: #9ca3af; font-style: italic;">
                Your response will appear here after submitting a query...
            </div>
        """, unsafe_allow_html=True)

# Footer with academic theme
st.markdown("---")
st.markdown("""
    <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                text-align: center; color: #4b5563; font-weight: bold; 
                padding: 25px; margin-top: 30px; border-radius: 10px;
                border-top: 3px solid #9ca3af;">
        <p style="font-size: 1.3rem; margin-bottom: 8px;">🎓 CSCLM - Cloud Computing Learning Module</p>
        <p style="font-size: 1.05rem; margin-bottom: 12px;">B.E. Computer Science | B.Tech Information Technology</p>
        <p style="font-size: 0.95rem; color: #6b7280;">License: MIT | Powered by OpenRouter API & Qwen AI</p>
    </div>
""", unsafe_allow_html=True)
