"""
AI Investment Debate Arena - Main Streamlit App
"""
import streamlit as st
import time
from datetime import datetime
from agents.researcher_agent import ResearcherAgent
from agents.bull_agent import BullAgent
from agents.bear_agent import BearAgent
from agents.judge_agent import JudgeAgent
from utils.helpers import save_debate_history, load_debate_history

# Page Config
st.set_page_config(
    page_title="AI Investment Debate Arena",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .verdict-buy {
        background-color: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    .verdict-sell {
        background-color: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    .verdict-hold {
        background-color: #f59e0b;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    .bull-card {
        border-left: 4px solid #10b981;
        padding: 1rem;
        background-color: #f0fdf4;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .bear-card {
        border-left: 4px solid #ef4444;
        padding: 1rem;
        background-color: #fef2f2;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .judge-card {
        border-left: 4px solid #8b5cf6;
        padding: 1rem;
        background-color: #f5f3ff;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'debate_history' not in st.session_state:
    st.session_state.debate_history = []
if 'current_debate' not in st.session_state:
    st.session_state.current_debate = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/investment-portfolio.png", width=80)
    st.title("🏆 Debate Arena")
    
    st.markdown("### 📈 Enter Stock Ticker")
    ticker = st.text_input("Ticker Symbol", value="AAPL", help="Enter a valid stock ticker").upper()
    
    st.markdown("---")
    st.markdown("### 🤖 Powered By")
    st.markdown("**Groq (Llama 3)**")
    
    debate_button = st.button(
        "⚡ Start Debate",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.is_running
    )
    
    st.markdown("---")
    
    st.markdown("### 📜 Debate History")
    history = load_debate_history()
    if history:
        for entry in reversed(history[-5:]):
            timestamp = entry.get('timestamp', '')[:16]
            ticker_name = entry.get('ticker', '')
            verdict = entry.get('verdict', {}).get('verdict', '')
            if verdict:
                emoji = "🟢" if verdict.upper() == "BUY" else "🔴" if verdict.upper() == "SELL" else "🟡"
                st.write(f"{emoji} {ticker_name} - {verdict} ({timestamp})")
    else:
        st.write("No debates yet. Start one!")

# Main Content
st.title("🏆 AI Investment Debate Arena")
st.markdown("#### 🎯 Bull vs Bear - Who will win?")

def run_debate(ticker):
    """Run the complete debate pipeline"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Research
    status_text.text("🔍 Researching stock data...")
    progress_bar.progress(20)
    
    researcher = ResearcherAgent()
    research = researcher.generate_response({"ticker": ticker})
    
    if "error" in research:
        st.error(f"Failed to research {ticker}: {research['error']}")
        return None
    
    # Step 2: Bull Case
    status_text.text("🐂 Building Bull Case...")
    progress_bar.progress(40)
    
    bull_agent = BullAgent()
    bull = bull_agent.generate_response({
        "ticker": ticker,
        "research": research
    })
    
    # Step 3: Bear Case
    status_text.text("🐻 Building Bear Case...")
    progress_bar.progress(60)
    
    bear_agent = BearAgent()
    bear = bear_agent.generate_response({
        "ticker": ticker,
        "research": research
    })
    
    # Step 4: Judge
    status_text.text("⚖️ Rendering Verdict...")
    progress_bar.progress(80)
    
    judge_agent = JudgeAgent()
    verdict = judge_agent.generate_response({
        "ticker": ticker,
        "research": research,
        "bull_arguments": bull,
        "bear_arguments": bear
    })
    
    progress_bar.progress(100)
    status_text.text("✅ Debate Complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()
    
    debate_data = {
        "ticker": ticker,
        "model": "groq",
        "research": research,
        "bull": bull,
        "bear": bear,
        "verdict": verdict,
        "timestamp": datetime.now().isoformat()
    }
    
    save_debate_history(debate_data)
    return debate_data

# Main Logic
if debate_button and ticker:
    st.session_state.is_running = True
    
    with st.spinner("🧠 Agents are debating..."):
        result = run_debate(ticker)
        if result:
            st.session_state.current_debate = result
            st.rerun()
    
    st.session_state.is_running = False

# Display Results
if st.session_state.current_debate:
    debate = st.session_state.current_debate
    verdict = debate.get("verdict", {})
    bull = debate.get("bull", {})
    bear = debate.get("bear", {})
    research = debate.get("research", {})
    
    # Verdict Banner
    verdict_text = verdict.get("verdict", "HOLD")
    confidence = verdict.get("confidence", 50)
    
    # Convert confidence to percentage if it's a decimal
    if isinstance(confidence, float) and confidence < 1:
        confidence = confidence * 100
    
    st.markdown(f"""
    <div class="verdict-{verdict_text.lower()}">
        {verdict_text} - {confidence:.0f}% Confidence
    </div>
    """, unsafe_allow_html=True)
    
    # Price Target Strip
    price_min = verdict.get("price_target_min", 0)
    price_max = verdict.get("price_target_max", 0)
    current_price = research.get("raw_stock_data", {}).get("current_price", 0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"${current_price:.2f}" if current_price else "N/A")
    
    with col2:
        bull_price = bull.get('price_target', 0)
        if bull_price and isinstance(bull_price, (int, float)):
            st.metric("Bull Target", f"${bull_price:.2f}")
        else:
            st.metric("Bull Target", "N/A")
    
    with col3:
        bear_price = bear.get('price_target', 0)
        if bear_price and isinstance(bear_price, (int, float)):
            st.metric("Bear Target", f"${bear_price:.2f}")
        else:
            st.metric("Bear Target", "N/A")
    
    with col4:
        if price_min and price_max and isinstance(price_min, (int, float)) and isinstance(price_max, (int, float)):
            st.metric("Judge's Range", f"${price_min:.2f} - ${price_max:.2f}")
        else:
            st.metric("Judge's Range", "N/A")
    
    st.markdown("---")
    
    # Clash Points
    clash_points = verdict.get("clash_points", [])
    if clash_points:
        st.markdown("### ⚔️ Key Clash Points")
        for point in clash_points:
            st.warning(f"⚡ {point}")
    
    # Three Columns: Bull, Bear, Judge
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🐂 Bull Case")
        with st.container():
            st.markdown(f"**Thesis:** {bull.get('thesis', 'N/A')}")
            st.markdown("**Growth Drivers:**")
            for driver in bull.get('growth_drivers', []):
                st.markdown(f"✅ {driver}")
            st.markdown("**Advantages:**")
            for adv in bull.get('advantages', []):
                st.markdown(f"💪 {adv}")
            bull_price = bull.get('price_target', 0)
            if bull_price and isinstance(bull_price, (int, float)):
                st.markdown(f"**Price Target:** ${bull_price:.2f}")
            else:
                st.markdown(f"**Price Target:** {bull_price}")
    
    with col2:
        st.markdown("### 🐻 Bear Case")
        with st.container():
            st.markdown(f"**Thesis:** {bear.get('thesis', 'N/A')}")
            st.markdown("**Risks:**")
            for risk in bear.get('risks', []):
                st.markdown(f"⚠️ {risk}")
            st.markdown("**Disadvantages:**")
            for dis in bear.get('disadvantages', []):
                st.markdown(f"📉 {dis}")
            bear_price = bear.get('price_target', 0)
            if bear_price and isinstance(bear_price, (int, float)):
                st.markdown(f"**Price Target:** ${bear_price:.2f}")
            else:
                st.markdown(f"**Price Target:** {bear_price}")
    
    with col3:
        st.markdown("### ⚖️ Judge's Analysis")
        with st.container():
            st.markdown(f"**Verdict:** {verdict.get('verdict', 'N/A')}")
            st.markdown(f"**Confidence:** {verdict.get('confidence', 0)}%")
            st.markdown(f"**Reasoning:** {verdict.get('reasoning', 'N/A')}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    Made with ❤️ by SoftCr8orsOfficial<br>
    Powered by Groq Llama 3 • Data from Yahoo Finance
</div>
""", unsafe_allow_html=True)
