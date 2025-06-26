# Stock News Summarization Project

This project uses the OpenRouter API with Perplexity Sonar Reasoning Pro to summarize recent news and provide short-term forecasts for multiple stock tickers.

## Prerequisites

- Python 3.12 
- OpenRouter API key (see .env setup below)
- `.env` file with your API key

## .env File Setup

Create a file named `.env` in the project root directory with the following content:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Replace `your_openrouter_api_key_here` with your actual OpenRouter API key. This key is required for the script to access the OpenRouter API.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Files

Make sure you have these files in your project directory:
- `stock_news_summary.py` - Main script using Perplexity Sonar Reasoning Pro
- `stock_news_summary_grok3.py` - Alternative script using Grok3 (x-ai/grok-3)
- `tickers.txt` - List of stock tickers to process
- `requirements.txt` - Python dependencies

### 3. Run the Scripts

You can use either script, depending on which model you want to use:

**To use Perplexity Sonar Reasoning Pro:**
```bash
python stock_news_summary.py
```

**To use Grok3 (x-ai/grok-3):**
```bash
python stock_news_summary_grok3.py
```

Each script must be run separately. Both use the same prompts and logic, but differ in the model used for summarization and forecasting.

## What the Scripts Do

1. **Reads tickers** from `tickers.txt` (e.g., PLTR, TSLA, NVDA, etc.)
2. **Processes each stock** with rate limiting (1 request per minute to avoid API overload)
3. **Gets two types of data** for each stock:
   - Recent news summary
   - Short-term forecast and key drivers
4. **Saves results** to a CSV file with timestamp (e.g., `stock_summaries_20250626_031106.csv` or `stock_summaries_grok3_20250626_031106.csv`)

## Output Format

The CSV file contains these columns:
- `CreatedAt` - When the entry was created
- `UpdatedAt` - When the entry was last updated
- `Symbol` - Stock ticker symbol
- `Last_UpdatedAt` - Timestamp of last update
- `Content` - The actual content (News or Forecast)

## Expected Runtime

- **Total time**: ~90 minutes for all 46 stocks
- **Rate limiting**: 1 request per minute to respect API limits
- **Progress tracking**: Shows which stock is being processed

## Files Generated

- `stock_summaries_YYYYMMDD_HHMMSS.csv` - Output from Perplexity script
- `stock_summaries_grok3_YYYYMMDD_HHMMSS.csv` - Output from Grok3 script

## Troubleshooting

- If you get permission errors, try running PowerShell as Administrator
- If the script stops, you can restart it - it will create a new CSV file
- Check your internet connection as the script makes API calls

## Example Output

```
Created CSV file: stock_summaries_grok3_20250626_031106.csv
Found 46 tickers to process.
Rate limiting: 1 request per minute to avoid API overload.
Results will be saved to: stock_summaries_grok3_20250626_031106.csv
==================================================

Processing 1/46: PLTR
  Getting news for PLTR...
  Waiting 60 seconds before next request...
  Getting forecast for PLTR...
  Saved data for PLTR to CSV
  Waiting 60 seconds before next ticker... 