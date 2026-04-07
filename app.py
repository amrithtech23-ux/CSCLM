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
    
    /* Main title styling */
    .main-title {
        color: #4169E1;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Suggestion prompt styling - Gray, Bold, Bigger */
    .suggestion-button {
        background-color: #f5f5f5;
        color: #4a4a4a;
        font-size: 1.15rem;
        font-weight: bold;
        padding: 15px 20px;
        margin: 8px 0;
        border-radius: 8px;
        border: 2px solid #d0d0d0;
        text-align: left;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .suggestion-button:hover {
        background-color: #e8e8e8;
        border-color: #4169E1;
        transform: translateX(5px);
    }
    
    /* Input text area styling */
    .stTextArea textarea {
        background-color: #ffffff;
        color: #333333;
        font-weight: bold;
        font-size: 1.1rem;
        border: 3px solid #4169E1;
        border-radius: 8px;
    }
    
    /* Result text area styling */
    .result-area {
        background-color: #1E3A8A;
        color: white;
        padding: 25px;
        border-radius: 10px;
        border: 3px solid #4169E1;
        font-weight: bold;
        font-size: 1.1rem;
        min-height: 300px;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4169E1;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: 3px solid #4169E1;
        padding: 12px 30px;
        border-radius: 8px;
    }
    
    .stButton > button:hover {
        background-color: #1E3A8A;
        border-color: #1E3A8A;
    }
    
    /* Section headers */
    .section-header {
        color: #4169E1;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #4169E1;
    }
    
    /* Info box */
    .info-box {
        background-color: #f0f8ff;
        border-left: 5px solid #4169E1;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Cloud Computing topics from knowledge base
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
    st.info("🎓 **For:** B.E. CS / B.Tech IT Students & Job Seekers")

# Main Title
st.markdown('<p class="main-title">⚖️ CLOUD COMPUTING for B.E.Computer Science/B.Tech Information Technology Chatbot</p>', unsafe_allow_html=True)

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
    
    # Display 10 random suggestions with gray, bold, bigger font
    for i, suggestion in enumerate(st.session_state.suggestions):
        # Create button with custom styling
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
            <div class="result-area" style="color: #a0aec0; font-style: italic;">
                Your response will appear here after submitting a query...
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #4169E1; font-weight: bold; padding: 20px; margin-top: 30px;">
        <p style="font-size: 1.2rem;">🎓 CSCLM - Cloud Computing Learning Module</p>
        <p>B.E. Computer Science | B.Tech Information Technology</p>
        <p style="font-size: 0.9rem; margin-top: 10px;">License: MIT | Powered by OpenRouter API & Qwen AI</p>
    </div>
""", unsafe_allow_html=True)
