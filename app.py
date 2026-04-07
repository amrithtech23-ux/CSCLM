import streamlit as st
import requests
import json
import random

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
    .stTextInput > div > div > input {
        background-color: #4169E1 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: 3px solid #4169E1 !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: 3px solid #4169E1 !important;
        min-height: 300px !important;
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

# Cloud Computing sample topics for generating suggestions
cloud_topics = [
    "Explain the evolution from centralized to distributed systems in cloud computing",
    "What are the differences between client-server and peer-to-peer architecture?",
    "Describe clustered computing types: high availability, load balancing, and HPC",
    "How does grid computing differ from cloud computing?",
    "Explain utility computing and the pay-per-use model",
    "What role does virtualization play in cloud computing?",
    "Describe Service-Oriented Architecture (SOA) in cloud environments",
    "Compare REST and SOAP web services for cloud interoperability",
    "What are the performance trade-offs between Docker containers and virtual machines?",
    "Explain microservices architecture and how it decomposes monolithic applications",
    "What is serverless computing (FaaS) and how does it work?",
    "Describe Software-Defined Networking (SDN) for cloud data centers",
    "What is Network Function Virtualization (NFV) in telecom clouds?",
    "Explain message queuing systems like RabbitMQ and Kafka for distributed communication",
    "How do Remote Procedure Calls (RPC/gRPC) work in cloud-native applications?",
    "What are REST constraints for building scalable APIs?",
    "Describe edge computing and how it extends network-based systems",
    "What is fog computing and its role between edge and cloud?",
    "How do Content Delivery Networks (CDN) work as distributed systems?",
    "Explain blockchain as a distributed ledger technology in cloud",
    "Describe distributed databases like Cassandra and CockroachDB",
    "What are in-memory data grids (Redis, Hazelcast) and their performance benefits?",
    "Explain distributed file systems like Ceph and GlusterFS",
    "What are consensus algorithms (Paxos, Raft) in cloud systems?",
    "Describe leader election and distributed coordination with ZooKeeper",
    "Compare distributed transactions: Two-phase commit (2PC) vs Saga pattern",
    "Explain the CAP theorem and its implications for cloud design",
    "What are the fallacies of distributed computing?",
    "Describe Google's Borg and Omega schedulers",
    "Explain Amazon DynamoDB's distributed architecture"
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
    api_key_input = st.text_input(
        "OpenRouter API Key",
        type="password",
        help="Enter your OpenRouter API Key or it will be loaded from secrets"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    # Try to load from secrets if not provided
    if not st.session_state.api_key:
        try:
            from streamlit import secrets
            st.session_state.api_key = secrets["OPENROUTER_API_KEY"]
            st.success("API Key loaded from secrets!")
        except:
            st.warning("Please enter your API Key or configure it in .streamlit/secrets.toml")
    
    st.markdown("---")
    st.info("**Target Audience:**\n- B.E. Computer Science Students\n- B.Tech IT Students\n- IT Job Seekers")
    
    st.markdown("---")
    st.markdown("**About:**\nThis chatbot helps you learn Cloud Computing concepts using Qwen AI model via OpenRouter API.")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💡 Suggested Prompts (Click to Use)")
    
    # Generate 10 random suggestions
    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
    
    # Display suggestions as clickable buttons
    for i, suggestion in enumerate(st.session_state.suggestions):
        if st.button(f"📌 {i+1}. {suggestion[:80]}...", key=f"sugg_{i}", use_container_width=True):
            st.session_state.query = suggestion
            st.rerun()
    
    if st.button("🔄 Refresh Suggestions", key="refresh_suggestions"):
        st.session_state.suggestions = random.sample(cloud_topics, min(10, len(cloud_topics)))
        st.rerun()

with col2:
    st.subheader("💬 Enter Your Query")
    
    # User query input
    user_query = st.text_area(
        "Type your Cloud Computing question here:",
        value=st.session_state.query,
        height=100,
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
            st.error("❌ Please provide an OpenRouter API Key in the sidebar or secrets file.")
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
                        "model": "qwen/qwen-2.5-72b-instruct",  # Using Qwen model
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
            <div style="background-color: #1E3A8A; color: white; padding: 20px; 
                        border-radius: 10px; border: 3px solid #4169E1; 
                        font-weight: bold; font-size: 1.1rem;">
            {st.session_state.result}
            </div>
        """, unsafe_allow_html=True)
        
        # Copy to clipboard button
        if st.button("📋 Copy Response"):
            st.write("Response copied to clipboard! (Use Ctrl+C to copy from the text above)")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #4169E1; font-weight: bold; padding: 20px;">
        <p>🎓 CSCLM - Cloud Computing Learning Module 🎓</p>
        <p>Built for B.E. Computer Science & B.Tech IT Students</p>
        <p>License: MIT | Powered by OpenRouter API & Qwen AI</p>
    </div>
""", unsafe_allow_html=True)`1
