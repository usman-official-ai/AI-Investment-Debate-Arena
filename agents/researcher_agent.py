"""
Researcher Agent - Fetches and analyzes stock data
"""
from typing import Dict, Any
from utils.data_fetcher import DataFetcher
from .base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    """Agent responsible for researching stock"""
    
    def __init__(self):
        super().__init__(
            name="Researcher",
            role="You are a professional financial researcher with expertise in fundamental and technical analysis. Provide objective, data-driven research."
        )
        self.data_fetcher = DataFetcher()
    
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate research report"""
        ticker = context.get("ticker", "")
        
        if not ticker:
            return {"error": "No ticker provided"}
        
        # Fetch stock data
        stock_data = self.data_fetcher.get_stock_data(ticker)
        fundamentals = self.data_fetcher.get_fundamentals(ticker)
        
        if not stock_data:
            return {"error": f"Could not fetch data for {ticker}"}
        
        # Generate research report
        prompt = f"""
        Analyze the following stock data for {ticker}:
        
        Stock Data:
        - Current Price: ${stock_data.get('current_price', 'N/A')}
        - Market Cap: ${stock_data.get('market_cap', 'N/A')}
        - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
        - 52 Week High: ${stock_data.get('fifty_two_week_high', 'N/A')}
        - 52 Week Low: ${stock_data.get('fifty_two_week_low', 'N/A')}
        - Volume: {stock_data.get('volume', 'N/A')}
        - Sector: {stock_data.get('sector', 'N/A')}
        - Industry: {stock_data.get('industry', 'N/A')}
        
        Fundamentals:
        - Revenue: ${fundamentals.get('revenue', 'N/A')}
        - Profit Margin: {fundamentals.get('profit_margin', 'N/A')}%
        - EPS: {fundamentals.get('eps', 'N/A')}
        - Debt: ${fundamentals.get('debt', 'N/A')}
        - Cash: ${fundamentals.get('cash', 'N/A')}
        - Growth: {fundamentals.get('growth', 'N/A')}%
        - Analyst Target: ${fundamentals.get('target_price', 'N/A')}
        
        Provide:
        1. Company Overview
        2. Financial Health Assessment
        3. Key Metrics Analysis
        4. Industry Context
        
        Return ONLY JSON with these fields: company_overview, financial_health, key_metrics, industry_context
        """
        
        response = self._call_llm(prompt)
        parsed = self._parse_json_response(response)
        parsed["raw_stock_data"] = stock_data
        parsed["raw_fundamentals"] = fundamentals
        parsed["ticker"] = ticker
        
        return parsed