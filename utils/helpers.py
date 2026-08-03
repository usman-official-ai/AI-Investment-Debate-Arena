"""
Helper utilities
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List

def save_debate_history(debate_data: Dict[str, Any], file_path: str = "data/debates/history.json"):
    """Save debate to history"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    debate_data['timestamp'] = datetime.now().isoformat()
    history.append(debate_data)
    history = history[-100:]
    
    with open(file_path, 'w') as f:
        json.dump(history, f, indent=2)

def load_debate_history(file_path: str = "data/debates/history.json") -> List[Dict[str, Any]]:
    """Load debate history"""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def format_currency(value: float) -> str:
    """Format currency value"""
    if value >= 1e12:
        return f"${value/1e12:.2f}T"
    elif value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.2f}"