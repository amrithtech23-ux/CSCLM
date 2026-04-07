import streamlit as st
import requests
import json
import random

# Page configuration
st.set_page_config(
    page_title="⚖️ Cloud Computing Chatbot",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[data-testid="baseButton-header"] {visibility: hidden;}
    
    /* Main Title - Style like Ref 1 */
    .main-title {
        color: #1e293b; /* Dark Slate/Black */
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        margin: 20px 0 10px 0;
        padding: 15px;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        letter-spacing: -0.5px;
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

    /* Suggestion Buttons - Style like Ref 2 */
    .suggestion-grid-btn {
        background-color: #64748b; /* Slate Gray */
        color: white;
        font-size: 1rem;
        font-weight: 500;
        padding: 18px;
        margin: 8px 0;
        border-radius: 10px;
        border: none;
        text-align: center;
        width: 100%;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
    }
    
    .suggestion-grid-btn:hover {
        background-color: #475569;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
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
    
    /* Submit Button */
    .submit-btn > button {
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        width: 100%;
    }

    /* Reset Button */
    .reset-btn > button {
        background-color: #ef4444;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        width: 100%;
    }

    /* Result Area */
    .result-area {
        background-color: #f8fafc;
        color: #334155;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-top: 20px;
        white-space: pre-wrap;
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

# Session State
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = random.sample(cloud_topics, 10)

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

# --- UI Layout ---

# 1. Title Section (Like Ref 1)
st.markdown('<p class="main-title">⚖️ Cloud Computing Chatbot</p>', unsafe_allow_html=True)

# 2. Info Bars
st.markdown('<p class="info-bar">🎯 <strong>Target Audience:</strong> B.E. CS / B.Tech IT Engineering Students & IT Industry Job Seekers</p>', unsafe_allow_html=True)
st.markdown('<p class="knowledge-bar">📚 <strong>Knowledge Base:</strong> ** loaded with comprehensive Cloud Computing topics across all units</p>', unsafe_allow_html=True)

# 3. Input Section
st.markdown('<p class="section-header">📝 Enter Your Query</p>', unsafe_allow_html=True)

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
                    st.session_state.result = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Response received!")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display Result if exists
if st.session_state.result:
    st.markdown('<p class="section-header">📚 Response</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="result-area">
        {st.session_state.result}
        </div>
    """, unsafe_allow_html=True)

# 5. Suggestions Section (MOVED BELOW RESULT - Style like Ref 2)
st.markdown('<p class="section-header">💡 System Suggestion Prompts</p>', unsafe_allow_html=True)

# Create a grid of suggestions (2 columns)
for i in range(0, len(st.session_state.suggestions), 2):
    cols = st.columns(2)
    
    # First item in the pair
    suggestion_1 = st.session_state.suggestions[i]
    with cols[0]:
        if st.button(f"• {suggestion_1}", key=f"sugg_{i}", use_container_width=True):
            st.session_state.query = suggestion_1
            st.rerun()
            
    # Second item in the pair (if exists)
    if i + 1 < len(st.session_state.suggestions):
        suggestion_2 = st.session_state.suggestions[i+1]
        with cols[1]:
            if st.button(f"• {suggestion_2}", key=f"sugg_{i+1}", use_container_width=True):
                st.session_state.query = suggestion_2
                st.rerun()

# Refresh Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Refresh Suggestions", use_container_width=True):
    st.session_state.suggestions = random.sample(cloud_topics, 10)
    st.rerun()

# Reset Logic
if reset_btn:
    st.session_state.query = ""
    st.session_state.result = ""
    st.session_state.suggestions = random.sample(cloud_topics, 10)
    st.rerun()
