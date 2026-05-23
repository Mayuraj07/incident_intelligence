import streamlit as st
import requests

st.set_page_config(
    page_title="Incident Intelligence Agent",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stApp { background-color: #F4F6F9; }
    
    .header-box {
        background-color: #0A2342;
        padding: 24px 32px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
    .header-box h1 {
        color: #FFFFFF;
        font-size: 26px;
        margin: 0;
        font-family: Arial;
    }
    .header-box p {
        color: #A8BDD4;
        font-size: 14px;
        margin: 6px 0 0 0;
        font-family: Arial;
    }
    .result-card {
        background-color: #FFFFFF;
        border: 1px solid #D6E0EE;
        border-left: 4px solid #0A2342;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .result-card h4 {
        color: #0A2342;
        margin: 0 0 6px 0;
        font-size: 14px;
        font-family: Arial;
    }
    .result-card p {
        color: #444;
        font-size: 13px;
        margin: 4px 0;
        font-family: Arial;
    }
    .similarity-badge {
        background-color: #E8EEF7;
        color: #0A2342;
        font-size: 12px;
        font-weight: bold;
        padding: 2px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .section-title {
        color: #0A2342;
        font-size: 16px;
        font-weight: bold;
        font-family: Arial;
        border-bottom: 2px solid #0A2342;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }
    .ai-box {
        background-color: #EEF3FB;
        border: 1px solid #C2D3EC;
        border-radius: 6px;
        padding: 20px 24px;
        color: #1a1a2e;
        font-size: 14px;
        font-family: Arial;
        line-height: 1.7;
    }
    .tab-label {
        font-size: 14px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-box">
        <h1>🏦 Incident Intelligence Agent</h1>
        <p>AI-powered investigation tool for banking reconciliation breaks · Powered by RAG + GPT-4o-mini</p>
    </div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🔍  Investigate a Break", "📋  All Incidents"])

# ── TAB 1: INVESTIGATE ──────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Describe the incident</div>', 
                unsafe_allow_html=True)
    
    query = st.text_area(
        label="",
        placeholder="e.g. SWIFT feed not received by EOD, nostro balance off by 2.4M USD in GLRS...",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        run = st.button("🔍 Investigate", use_container_width=True)
    with col2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.rerun()

    if run and query.strip():
        with st.spinner("Searching similar incidents and generating analysis..."):
            try:
                response = requests.post(
                    "http://localhost:8001/investigate",
                    json={"description": query}
                )
                data = response.json()

                st.markdown("<br>", unsafe_allow_html=True)
                
                # AI Analysis
                st.markdown('<div class="section-title">AI Investigation Report</div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="ai-box">{data["investigation"]}</div>',
                            unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Similar Incidents
                st.markdown('<div class="section-title">5 Most Similar Past Incidents</div>',
                            unsafe_allow_html=True)
                
                for inc in data["similar_incidents"]:
                    similarity_pct = round(inc["similarity"] * 100, 1)
                    st.markdown(f"""
                        <div class="result-card">
                            <span class="similarity-badge">Match {similarity_pct}%</span>
                            <h4>{inc["incident_id"]} — {inc["description"]}</h4>
                            <p><b>Root cause:</b> {inc["root_cause"]}</p>
                            <p><b>Resolution:</b> {inc["resolution"]}</p>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Could not connect to API. Make sure FastAPI is running. Error: {e}")

    elif run and not query.strip():
        st.warning("Please describe the incident before investigating.")

# ── TAB 2: ALL INCIDENTS ────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Incident Knowledge Base</div>',
                unsafe_allow_html=True)
    
    try:
        response = requests.get("http://localhost:8001/incidents")
        incidents = response.json()
        
        st.markdown(f"**{len(incidents)} incidents in the knowledge base**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        import pandas as pd
        df = pd.DataFrame(incidents)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    except Exception as e:
        st.error(f"Could not load incidents. Make sure FastAPI is running. Error: {e}")