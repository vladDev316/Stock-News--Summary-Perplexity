import requests
import json
import time
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Prompts
def get_news_prompt(ticker):
    return f"Most recent news on {ticker} in bullets. only include bullets. Rephrase any statements to not include X, X post or X users if X the platform is mentioned. each bullet formatted as topic: content."

def get_forecast_prompt(ticker):
    return f"Short term forecast range and key drivers of {ticker} in bullets. only include bullets. Rephrase any statements to not include X, X post or X users if X the platform is mentioned. each bullet formatted as topic: content."

# Function to call OpenRouter API
def get_openrouter_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://twitter.com/",
        # "X-Title": "Stock News Summarizer",
    }
    data = {
        "model": "perplexity/sonar-reasoning-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        # Extract the response text
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "[Error] Unexpected response format."
    else:
        return f"[Error] API request failed: {response.status_code} {response.text}"

def read_tickers_from_file(filename):
    """Read tickers from tickers.txt file"""
    try:
        with open(filename, 'r') as file:
            tickers = [line.strip() for line in file if line.strip()]
        return tickers
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []

def create_csv_file(filename):
    """Create CSV file with headers"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CreatedAt', 'UpdatedAt', 'Symbol', 'Last_UpdatedAt', 'Content'])
    print(f"Created CSV file: {filename}")

def append_to_csv(filename, symbol, content_type, content):
    """Append a row to the CSV file"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            current_time,  # CreatedAt
            current_time,  # UpdatedAt
            symbol,        # Symbol
            current_time,  # Last_UpdatedAt
            f"{content_type}: {content}"  # Content
        ])

def main():
    # Read tickers from file
    tickers = read_tickers_from_file('tickers.txt')
    
    if not tickers:
        print("No tickers found. Please check tickers.txt file.")
        return
    
    # Create CSV file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"stock_summaries_{timestamp}.csv"
    create_csv_file(csv_filename)
    
    print(f"Found {len(tickers)} tickers to process.")
    print("Rate limiting: 1 request per minute to avoid API overload.")
    print(f"Results will be saved to: {csv_filename}")
    print("=" * 50)
    
    for i, ticker in enumerate(tickers, 1):
        print(f"\nProcessing {i}/{len(tickers)}: {ticker}")
        
        try:
            # Get news
            print(f"  Getting news for {ticker}...")
            news = get_openrouter_response(get_news_prompt(ticker))
            append_to_csv(csv_filename, ticker, "News", news)
            
            # Wait 60 seconds before next request
            print("  Waiting 60 seconds before next request...")
            time.sleep(60)
            
            # Get forecast
            print(f"  Getting forecast for {ticker}...")
            forecast = get_openrouter_response(get_forecast_prompt(ticker))
            append_to_csv(csv_filename, ticker, "Forecast", forecast)
            
            print(f"  Saved data for {ticker} to CSV")
            
            # Wait 60 seconds before next ticker (except for the last one)
            if i < len(tickers):
                print("  Waiting 60 seconds before next ticker...")
                time.sleep(60)
                
        except Exception as e:
            print(f"  Error processing {ticker}: {str(e)}")
            # Still append error to CSV for tracking
            append_to_csv(csv_filename, ticker, "Error", str(e))
            continue
    
    print(f"\nCompleted processing {len(tickers)} tickers!")
    print(f"All results saved to: {csv_filename}")

if __name__ == "__main__":
    main() 