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

# Define the expected categories
NEWS_CATEGORIES = [
    "Stock Performance",
    "Analyst Coverage",
    "Q1 2025 Performance",
    "Fund Flows",
    "Market Sentiment",
    "Technical Indicators",
    "Regulatory Adjustment",
    "Option Activity",
    "Investor Moves",
    "Economic Outlook"
]

FORECAST_CATEGORIES = [
    "Short-Term Price Forecast",
    "Three-Month Outlook",
    "Small-Cap Sentiment",
    "Technical Indicators",
    "Fund Flows",
    "Interest Rate Impact",
    "Options Activity",
    "Economic Policy"
]

def get_news_prompt(ticker):
    categories_str = "\n".join([f"- {cat}" for cat in NEWS_CATEGORIES])
    return f"""Analyze and summarize the most recent news for {ticker} in a structured format.
Please provide information for EACH of the following categories, using the exact format 'Category: Content':

{categories_str}

Rules:
1. Must include ALL categories listed above
2. Each category must have relevant content
3. If no specific information is available for a category, provide a general market context
4. Rephrase any statements to not include X, X post or X users if X the platform is mentioned
5. Keep each category's content concise and focused"""

def get_forecast_prompt(ticker):
    categories_str = "\n".join([f"- {cat}" for cat in FORECAST_CATEGORIES])
    return f"""Analyze and provide a structured forecast for {ticker} covering EACH of the following categories:

{categories_str}

Rules:
1. Must include ALL categories listed above
2. Each category must have relevant content
3. If no specific information is available for a category, provide a general market context
4. Rephrase any statements to not include X, X post or X users if X the platform is mentioned
5. Keep each category's content concise and focused
6. Format each line exactly as 'Category: Content'"""

def format_response_to_json(response_text, categories):
    """Convert the response text into a structured JSON format"""
    result = {}
    current_category = None
    
    for line in response_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check if this line starts with any of our categories
        for category in categories:
            if line.startswith(f"{category}:"):
                current_category = category
                content = line[len(f"{category}:"):].strip()
                result[category] = content
                break
    
    # Ensure all categories are present
    for category in categories:
        if category not in result:
            result[category] = "No specific information available"
    
    return result

def get_openrouter_response_perplexity(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://twitter.com/",
    }
    data = {
        "model": "perplexity/sonar-small-online",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
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
            json.dumps({content_type: content})  # Content as JSON
        ])

def main():
    # Read tickers from file
    tickers = read_tickers_from_file('tickers.txt')
    
    if not tickers:
        print("No tickers found. Please check tickers.txt file.")
        return
    
    # Create CSV file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"stock_summaries_perplexity_{timestamp}.csv"
    create_csv_file(csv_filename)
    
    print(f"Found {len(tickers)} tickers to process.")
    print("Rate limiting: 30 seconds between requests to avoid API overload.")
    print(f"Results will be saved to: {csv_filename}")
    print("=" * 50)
    
    for i, ticker in enumerate(tickers, 1):
        print(f"\nProcessing {i}/{len(tickers)}: {ticker}")
        
        try:
            # Get news
            print(f"  Getting news for {ticker}...")
            news_response = get_openrouter_response_perplexity(get_news_prompt(ticker))
            news_json = format_response_to_json(news_response, NEWS_CATEGORIES)
            append_to_csv(csv_filename, ticker, "news_summary_recent", news_json)
            
            # Wait 30 seconds before next request
            print("  Waiting 30 seconds before next request...")
            time.sleep(30)
            
            # Get forecast
            print(f"  Getting forecast for {ticker}...")
            forecast_response = get_openrouter_response_perplexity(get_forecast_prompt(ticker))
            forecast_json = format_response_to_json(forecast_response, FORECAST_CATEGORIES)
            append_to_csv(csv_filename, ticker, "forecast_range", forecast_json)
            
            print(f"  Saved data for {ticker} to CSV")
            
            # Wait 30 seconds before next ticker (except for the last one)
            if i < len(tickers):
                print("  Waiting 30 seconds before next ticker...")
                time.sleep(30)
                
        except Exception as e:
            print(f"  Error processing {ticker}: {str(e)}")
            # Still append error to CSV for tracking
            append_to_csv(csv_filename, ticker, "Error", str(e))
            continue
    
    print(f"\nCompleted processing {len(tickers)} tickers!")
    print(f"All results saved to: {csv_filename}")

if __name__ == "__main__":
    main() 