"""
Judge Agent - Renders final verdict
"""
from typing import Dict, Any
from .base_agent import BaseAgent

class JudgeAgent(BaseAgent):
    """Agent that renders final verdict"""
    
    def __init__(self):
        super().__init__(
            name="Judge",
            role="You are an impartial investment judge with experience in financial analysis. Weigh both sides fairly and render objective verdicts."
        )
    
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final verdict"""
        ticker = context.get("ticker", "")
        bull = context.get("bull_arguments", {})
        bear = context.get("bear_arguments", {})
        research = context.get("research", {})
        
        prompt = f"""
        As an impartial JUDGE, analyze the debate for {ticker}.
        
        BULL CASE:
        - Thesis: {bull.get('thesis', 'N/A')}
        - Growth Drivers: {bull.get('growth_drivers', [])}
        - Price Target: ${bull.get('price_target', 'N/A')}
        - Reasoning: {bull.get('reasoning', 'N/A')}
        
        BEAR CASE:
        - Thesis: {bear.get('thesis', 'N/A')}
        - Risks: {bear.get('risks', [])}
        - Price Target: ${bear.get('price_target', 'N/A')}
        - Reasoning: {bear.get('reasoning', 'N/A')}
        
        Research Data:
        - Current Price: ${research.get('raw_stock_data', {}).get('current_price', 'N/A')}
        - Market Cap: {research.get('raw_stock_data', {}).get('market_cap', 'N/A')}
        - P/E Ratio: {research.get('raw_stock_data', {}).get('pe_ratio', 'N/A')}
        - Growth: {research.get('raw_fundamentals', {}).get('growth', 'N/A')}%
        
        Provide:
        1. Final Verdict (BUY, SELL, or HOLD)
        2. Confidence Score (0-100)
        3. Price Target Range (minimum and maximum)
        4. Key Clash Points (where arguments conflict)
        5. Summary Reasoning
        
        Return ONLY JSON with: verdict, confidence, price_target_min, price_target_max, clash_points, reasoning
        """
        
        response = self._call_llm(prompt)
        return self._parse_json_response(response)