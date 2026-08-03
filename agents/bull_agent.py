"""
Bull Agent - Argues the bullish case
"""
from typing import Dict, Any
from .base_agent import BaseAgent

class BullAgent(BaseAgent):
    """Agent that argues the bull case"""
    
    def __init__(self):
        super().__init__(
            name="Bull",
            role="You are an optimistic investment analyst who sees opportunity in every situation. Argue the bullish case with conviction and data-backed reasoning."
        )
    
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bull case arguments"""
        ticker = context.get("ticker", "")
        research = context.get("research", {})
        
        prompt = f"""
        As a BULLISH INVESTMENT ANALYST, argue the bull case for {ticker}.
        
        Research Data:
        - Company: {research.get('company_overview', 'N/A')}
        - Industry: {research.get('industry_context', 'N/A')}
        - Current Price: ${research.get('raw_stock_data', {}).get('current_price', 'N/A')}
        - Market Cap: ${research.get('raw_stock_data', {}).get('market_cap', 'N/A')}
        - P/E Ratio: {research.get('raw_stock_data', {}).get('pe_ratio', 'N/A')}
        - Revenue Growth: {research.get('raw_fundamentals', {}).get('growth', 'N/A')}%
        - Profit Margin: {research.get('raw_fundamentals', {}).get('profit_margin', 'N/A')}%
        - Analyst Target: ${research.get('raw_fundamentals', {}).get('target_price', 'N/A')}
        
        Present a compelling case why {ticker} is a BUY.
        
        Include:
        1. Key Bullish Thesis
        2. Growth Drivers (3-4 points)
        3. Competitive Advantages
        4. Price Target Prediction
        5. Counter-arguments to potential bear points
        
        Return ONLY JSON with: thesis, growth_drivers, advantages, price_target, reasoning, counter_arguments
        """
        
        response = self._call_llm(prompt)
        return self._parse_json_response(response)