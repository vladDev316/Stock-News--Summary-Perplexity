# Stock News Summarization Project

This project uses the OpenRouter API with Perplexity Sonar Reasoning Pro to summarize recent news and provide short-term forecasts for multiple stock tickers.

## Prerequisites

- Python 3.7 or higher
- OpenRouter API key (already configured in the script)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Files

Make sure you have these files in your project directory:
- `stock_news_summary.py` - Main script
- `tickers.txt` - List of stock tickers to process
- `requirements.txt` - Python dependencies

### 3. Run the Script

```bash
python stock_news_summary.py
```

## What the Script Does

1. **Reads tickers** from `tickers.txt` (46 stocks including PLTR, TSLA, NVDA, etc.)
2. **Processes each stock** with rate limiting (1 request per minute to avoid API overload)
3. **Gets two types of data** for each stock:
   - Recent news summary
   - Short-term forecast and key drivers
4. **Saves results** to a CSV file with timestamp (e.g., `stock_summaries_20250626_031106.csv`)

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

- `stock_summaries_YYYYMMDD_HHMMSS.csv` - Main output file with all results

## Troubleshooting

- If you get permission errors, try running PowerShell as Administrator
- If the script stops, you can restart it - it will create a new CSV file
- Check your internet connection as the script makes API calls

## Example Output

```
Created CSV file: stock_summaries_20250626_031106.csv
Found 46 tickers to process.
Rate limiting: 1 request per minute to avoid API overload.
Results will be saved to: stock_summaries_20250626_031106.csv
==================================================

Processing 1/46: PLTR
  Getting news for PLTR...
  Waiting 60 seconds before next request...
  Getting forecast for PLTR...
  Saved data for PLTR to CSV
  Waiting 60 seconds before next ticker... 