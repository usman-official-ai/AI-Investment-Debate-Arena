"""
Data fetcher for stock information
"""
import yfinance as yf
import logging
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class DataFetcher:
    """Fetches stock data from Yahoo Finance"""
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch current stock data"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
                "volume": info.get("volume", 0),
                "avg_volume": info.get("averageVolume", 0),
                "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "description": info.get("longBusinessSummary", ""),
                "name": info.get("longName", ticker)
            }
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            return {}
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """Fetch fundamental data"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "revenue": info.get("totalRevenue", 0),
                "profit_margin": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else 0,
                "eps": info.get("trailingEps", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "debt": info.get("totalDebt", 0),
                "cash": info.get("totalCash", 0),
                "growth": info.get("earningsGrowth", 0) * 100 if info.get("earningsGrowth") else 0,
                "target_price": info.get("targetMeanPrice", 0)
            }
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {e}")
            return {}