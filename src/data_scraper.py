import json
from tqdm import tqdm
from datetime import datetime
import yfinance as yf
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
import pandas as pd
import time

load_dotenv()

def fetch_recent_news(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        
        news = stock.get_news(count=200)
        print(f"Fetching {ticker} news: {len(news)}")
        
        recent_news = []
        for article in tqdm(news):
            # print(article['content'])
            try:
                news = {
                    "title": article['content']['title'],
                    "link": article["content"]["thumbnail"]["originalUrl"] if article["content"]["thumbnail"] else article["content"]["canonicalUrl"]["url"] or None,
                    "published_at": article['content']['pubDate'],
                    "published_at_timestamp": int(datetime.fromisoformat(article['content']['pubDate'].replace("Z", "+00:00")).timestamp()),
                    "content": article['content']['summary']
                }
                recent_news.append(news)
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []
    
    return recent_news

def fetch_stock_data(
    tickers: List[str],
    start_date: str,
    end_date: str,
    interval: str = "1d",
    save_path: Optional[str] = None
) -> Dict[str, pd.DataFrame]:
    """
    Fetch historical stock price data for a list of ticker symbols.
    
    Args:
        tickers: List of ticker symbols (e.g., ["AAPL", "MSFT", "GOOGL"])
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        interval: Data interval ('1d', '1wk', '1mo', etc.)
        save_path: Optional path to save the data as CSV files
        
    Returns:
        Dictionary mapping ticker symbols to their respective price DataFrames
    """
    print(f"Fetching stock data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    stock_data = {}
    
    for ticker in tqdm(tickers, desc="Fetching stock data"):
        try:
            print(f"Fetching {ticker} stock data...")
            # Fetch data using yfinance
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False
            )
            
            if data.empty:
                print(f"No data found for {ticker}")
                continue
                
            # Add ticker column for identification
            data['Ticker'] = ticker
            
            # Calculate additional metrics
            data['Daily_Return'] = data['Close'].pct_change()
            data['Volatility_5d'] = data['Daily_Return'].rolling(window=5).std()
            
            # Store in dictionary
            stock_data[ticker] = data
            
            # Save to CSV if path is provided
            if save_path:
                os.makedirs(save_path, exist_ok=True)
                file_path = os.path.join(save_path, f"{ticker}_prices.csv")
                data.to_csv(file_path)
                print(f"Saved {ticker}'s stock data to {file_path}")
                
            print(f"Successfully fetched data for {ticker}: {len(data)} records")
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
        
        # Add delay to avoid rate limiting
        time.sleep(0.5)
    
    return stock_data

if __name__ == "__main__":
    # Create data directories if they don't exist
    data_dirs = [os.getenv("NEWS_DATA_PATH"), os.getenv("PRICE_DATA_PATH")]
    for data_dir in data_dirs:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            print(f"Created directory: {data_dir}")
        else:
            print(f"Directory already exists: {data_dir}")

    # Fetch stock data  
    tickers = os.getenv("TICKERS").split(",")
    fetch_stock_data(tickers, os.getenv("START_DATE"), os.getenv("END_DATE"), os.getenv("INTERVAL"), os.getenv("PRICE_DATA_PATH"))


    # Fetch news data
    recent_news_data = []
    for ticker in tickers:
        recent_news_data.append({"ticker": ticker, "news": fetch_recent_news(ticker)})

    with open(os.path.join("./data/news", f"recent_news_{datetime.now().strftime('%Y-%m-%d')}.json"), "w") as f:
        json.dump(recent_news_data, f)
    print(f"Saved news data to ./data/news/recent_news_{datetime.now().strftime('%Y-%m-%d')}.json")
