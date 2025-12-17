import streamlit as st
import requests
import time

# --- CONFIG ---
API_URL = "http://localhost:8000/research"
st.set_page_config(page_title="Sentinel AI", page_icon="🕵️‍♀️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .report-box {
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/search.png", width=100)
    st.title("🕵️‍♀️ Sentinel")
    st.caption("Autonomous Research Agent")
    
    st.divider()
    
    # 1. Capture User Inputs
    model_type = st.radio("Model Engine", ["Llama-3.3-70b (Groq)", "GPT-4o (Mock)"], index=0)
    search_mode = st.selectbox("Search Mode", ["Auto (Smart Router)", "Deep Research (ArXiv Only)", "Fast (Web Only)"])
    
    st.info(f"System Status: **Online**\n\nPipeline: **CI/CD Verified** ✅")

# --- MAIN UI ---
st.title("Research Mission Control")
st.markdown("Enter a complex topic. Sentinel will **Plan**, **Search**, **Critique**, and **Synthesize**.")

topic = st.text_input("Research Topic", placeholder="e.g., Impact of Quantum Computing on Encryption Standards")

# --- BUTTON CLICK LOGIC STARTS HERE ---
if st.button("🚀 Initialize Agent"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        # Create a placeholder for the "Thinking" state
        status_container = st.status("🕵️‍♀️ Sentinel Activated", expanded=True)
        
        try:
            with status_container:
                st.write("🔄 Initializing Planner Agent...")
                time.sleep(1) # Fake UX delay for effect
                st.write(f"🔍 Deploying Search Agents ({search_mode})...")
                
                # 2. Prepare the Payload with Sidebar Inputs
                payload = {
                    "topic": topic,
                    "search_mode": search_mode,
                    "model_type": model_type
                }
                
                # 3. Call Backend with Dynamic Payload
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.write("⚖️ Critic Agent reviewing findings...")
                    loop_count = data.get("loop_count", 0)
                    if loop_count > 0:
                        st.warning(f"⚠️ Critic rejected draft {loop_count} time(s). Self-correction triggered.")
                    else:
                        st.success("✅ Critic approved first draft.")
                        
                    st.write("📝 Synthesizing Final Report...")
                    status_container.update(label="Research Complete", state="complete", expanded=False)
                    
                    # --- DISPLAY RESULTS ---
                    
                    # Metrics Row
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Iterations", f"{loop_count + 1}", delta="Self-Corrections")
                    col2.metric("Sources Found", f"{len(data.get('sources', []))}")
                    col3.metric("Plan Steps", f"{len(data.get('plan', []))}")
                    
                    # Tabs for Report vs Logic
                    tab1, tab2, tab3 = st.tabs(["📄 Executive Summary", "🧠 Agent Logic", "📚 Sources"])
                    
                    with tab1:
                        st.markdown(f"### 📑 {topic}")
                        st.markdown(f"<div class='report-box'>{data['final_summary']}</div>", unsafe_allow_html=True)
                        
                    with tab2:
                        st.subheader("The Agent's Plan")
                        st.json(data.get("plan"))
                        
                        st.subheader("Execution Trace")
                        st.info("Check LangSmith Dashboard for full flame graph.")
                        st.json({"model_used": model_type, "search_strategy": search_mode})
                        
                    with tab3:
                        st.subheader("Citations")
                        for src in data.get("sources", []):
                            with st.expander(src[:100] + "..."):
                                st.text(src)

                else:
                    status_container.update(label="Mission Failed", state="error")
                    st.error(f"Error: {response.text}")
                    
        except Exception as e:
            st.error(f"Connection Error: {e}")