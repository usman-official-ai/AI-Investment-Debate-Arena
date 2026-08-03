# 🏆 AI Investment Debate Arena

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LLM-FF6B00.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered investment debate system where specialized agents argue both sides of a stock thesis and render a final verdict using **Groq API**.

## 🌐 Live Demo

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-app-url.streamlit.app/)

## 🧠 How It Works

1. **Researcher Agent** - Fetches and analyzes stock data
2. **Bull Agent** - Argues the bullish case with conviction
3. **Bear Agent** - Argues the bearish case with conviction
4. **Judge Agent** - Renders final verdict and price target

## ✨ Features

- 🎯 **Multi-Agent System**: Specialized agents for research, bull, bear, and judging
- 📊 **Real Stock Data**: Fetches live data from Yahoo Finance
- 🏆 **Verdict Rendering**: BUY, SELL, or HOLD with confidence score
- 💰 **Price Targets**: Bull, Bear, and Judge's range
- ⚔️ **Clash Points**: Key points where arguments conflict
- 📜 **Debate History**: Save and view past debates
- 🤖 **Groq Integration**: Powered by Llama 3

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Framework** | Streamlit |
| **AI Model** | Groq (Llama 3) |
| **Data** | Yahoo Finance API |
| **Language** | Python 3.9+ |

## 📋 Prerequisites

- Python 3.9+
- Groq API Key
2. Create virtual environment
bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up environment variables
Create .env file:

env
GROQ_API_KEY=your_groq_api_key_here
5. Run the application
bash
streamlit run app.py
📖 Usage Guide
Enter a stock ticker (e.g., AAPL, TSLA, MSFT)

Click "Start Debate"

Watch the agents analyze and debate

Review the final verdict and analysis

📁 Project Structure
text
AI-Investment-Debate-Arena/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── .env                  # Environment variables
├── config/
│   └── settings.py       # Configuration
├── agents/
│   ├── base_agent.py     # Base agent class
│   ├── researcher_agent.py
│   ├── bull_agent.py
│   ├── bear_agent.py
│   └── judge_agent.py
├── utils/
│   ├── data_fetcher.py   # Stock data fetching
│   └── helpers.py        # Utility functions
└── data/
    └── debates/          # Debate history storage
🚀 Deployment
Deploy on Streamlit Cloud
Push your code to GitHub

Go to share.streamlit.io

Click "New app"

Select your repository and branch

Set main file as app.py

Add your Groq API key in Streamlit secrets

Click "Deploy"

Environment Variables on Streamlit
Add to Streamlit secrets:

toml
GROQ_API_KEY = "your_groq_api_key_here"
👤 Author
Usman (@SoftCr8orsOfficial)

🌟 Show Your Support
If you found this project helpful, please give it a ⭐️ on GitHub!

