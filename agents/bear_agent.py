"""
Bear Agent - Argues the bearish case
"""
from typing import Dict, Any
from .base_agent import BaseAgent

class BearAgent(BaseAgent):
    """Agent that argues the bear case"""
    
    def __init__(self):
        super().__init__(
            name="Bear",
            role="You are a pessimistic investment analyst who sees risks in every opportunity. Argue the bearish case with conviction and data-backed reasoning."
        )
    
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bear case arguments"""
        ticker = context.get("ticker", "")
        research = context.get("research", {})
        
        prompt = f"""
        As a BEARISH INVESTMENT ANALYST, argue the bear case for {ticker}.
        
        Research Data:
        - Company: {research.get('company_overview', 'N/A')}
        - Industry: {research.get('industry_context', 'N/A')}
        - Current Price: ${research.get('raw_stock_data', {}).get('current_price', 'N/A')}
        - Market Cap: ${research.get('raw_stock_data', {}).get('market_cap', 'N/A')}
        - P/E Ratio: {research.get('raw_stock_data', {}).get('pe_ratio', 'N/A')}
        - Debt: ${research.get('raw_fundamentals', {}).get('debt', 'N/A')}
        - Profit Margin: {research.get('raw_fundamentals', {}).get('profit_margin', 'N/A')}%
        - Analyst Target: ${research.get('raw_fundamentals', {}).get('target_price', 'N/A')}
        
        Present a compelling case why {ticker} is a SELL.
        
        Include:
        1. Key Bearish Thesis
        2. Risks and Threats (3-4 points)
        3. Competitive Disadvantages
        4. Price Target Prediction
        5. Counter-arguments to potential bull points
        
        Return ONLY JSON with: thesis, risks, disadvantages, price_target, reasoning, counter_arguments
        """
        
        response = self._call_llm(prompt)
        return self._parse_json_response(response)