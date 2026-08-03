"""
Configuration settings for the Investment Debate Arena
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model Configuration
    GROQ_MODEL = "llama-3.3-70b-versatile"
    
    # Debate Configuration
    MAX_DEBATE_ROUNDS = 3
    
    # Data Storage
    HISTORY_FILE = "data/debates/history.json"

settings = Settings()