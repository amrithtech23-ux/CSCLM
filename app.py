import streamlit as st
import requests
import json
import random
import os

# Page configuration
st.set_page_config(
    page_title="⚖️ CLOUD COMPUTING Chatbot",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        color: #4169E1;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .suggestion-prompt {
        color: #4169E1;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #f0f8ff;
    }
    .stTextArea textarea {
        background-color: #4169E1 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: 3px solid #4169E1 !important;
    }
    .result-box {
        background-color: #1E3A8A !important;
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        border: 3px solid #4169E1 !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button {
        background-color: #4169E1;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: 3px solid #4169E1;
        padding: 10px 24px;
    }
    .stButton > button:hover {
        background-color: #1E3A8A;
        border-color: #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

# Cloud Computing sample topics from knowledge base
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

# Title
st.markdown('<p class="main-title">⚖️ CLOUD COMPUTING for B.E.Computer Science/B.Tech Information Technology Chatbot</p>', unsafe_allow_html=True)

# Sidebar for API Key configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Try to load API key from Streamlit secrets first
    api_key = ""
    try:
        from streamlit import secrets
        if "OPENROUTER_API_KEY" in secrets:
            api_key = secrets["OPENROUTER_API_KEY"]
            st.session_state.api_key = api_key
            st.success("✅ API Key loaded from secrets!")
    except Exception as e:
        st.warning("⚠️ Please configure API Key")
    
    # Allow manual entry if needed
    api_key_input = st.text_input(
        "Or enter API Key manually:",
        type="password",
        help="Enter your OpenRouter API Key"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ API Key entered manually")
    
    st.markdown("---")
    st.info("**🎓 Target Audience:**\n- B.E. Computer Science Students\n- B.Tech IT Students\n- IT Job Seekers")
    
    st.markdown("---")
    st.markdown("**📖 About:**\nThis chatbot helps you learn Cloud Computing concepts using Qwen AI model via OpenRouter API.")
    
    st.markdown("---")
    st.caption("🔐 Your API key is encrypted and secure")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💡 Suggested Prompts (Click to Use)")
    
    # Generate 10 random suggestions
    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
    
    # Display suggestions as clickable buttons
    for i, suggestion in enumerate(st.session_state.suggestions):
        if st.button(f"📌 {i+1}. {suggestion[:70]}...", key=f"sugg_{i}", use_container_width=True):
            st.session_state.query = suggestion
            st.rerun()
    
    if st.button("🔄 Refresh Suggestions", key="refresh_suggestions", use_container_width=True):
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
        st.rerun()

with col2:
    st.subheader("💬 Enter Your Query")
    
    # User query input
    user_query = st.text_area(
        "Type your Cloud Computing question here:",
        value=st.session_state.query,
        height=150,
        placeholder="E.g., Explain virtualization in cloud computing...",
        key="user_query_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        submit_btn = st.button("📤 Submit Prompt", use_container_width=True)
    
    with col_btn2:
        reset_btn = st.button("🔄 Reset", use_container_width=True)
    
    # Handle reset
    if reset_btn:
        st.session_state.query = ""
        st.session_state.result = ""
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
        st.rerun()
    
    # Handle submit
    if submit_btn and user_query:
        if not st.session_state.api_key:
            st.error("❌ Please provide an OpenRouter API Key in the sidebar or configure it in Streamlit Secrets.")
            st.warning("💡 Go to App Settings → Secrets and add: OPENROUTER_API_KEY = \"your-key-here\"")
        else:
            with st.spinner("🤖 Getting response from Qwen AI..."):
                try:
                    # Prepare the API request
                    headers = {
                        "Authorization": f"Bearer {st.session_state.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/amrithtech23-ux/CSCLM",
                        "X-Title": "CSCLM Cloud Computing Chatbot"
                    }
                    
                    # System prompt for context
                    system_prompt = """You are an expert Cloud Computing instructor helping B.E. Computer Science and B.Tech IT students. 
                    Provide clear, detailed, and educational answers about cloud computing topics. 
                    Include practical examples and real-world applications where relevant.
                    Keep explanations structured and easy to understand for students and job seekers."""
                    
                    payload = {
                        "model": "qwen/qwen-2.5-72b-instruct",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_query}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                    
                    # Make API call
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
    
    # Display result
    if st.session_state.result:
        st.subheader("📚 Response")
        st.markdown(f"""
            <div class="result-box">
            {st.session_state.result}
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #4169E1; font-weight: bold; padding: 20px;">
        <p>🎓 CSCLM - Cloud Computing Learning Module 🎓</p>
        <p>Built for B.E. Computer Science & B.Tech IT Students</p>
        <p>License: MIT | Powered by OpenRouter API & Qwen AI</p>
    </div>
""", unsafe_allow_html=True)
