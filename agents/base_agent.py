"""
Base Agent Class - All agents inherit from this
"""
import json
import logging
from typing import Dict, Any
from abc import ABC, abstractmethod
from groq import Groq
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all debate agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        
        # Initialize Groq Client
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_name = settings.GROQ_MODEL
        
        logger.info(f"🤖 {self.name} Agent initialized with Groq")
    
    @abstractmethod
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent response"""
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """Call Groq LLM with prompt"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.role},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Groq LLM: {e}")
            return ""
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON response from LLM"""
        try:
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            return json.loads(text)
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            return {"error": "Failed to parse JSON", "raw": text}