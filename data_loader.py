import pandas as pd
import requests

##################   Import data   ##################
def load_time_series_data(ticker):
    stock_api_url = 'https://www.alphavantage.co/query'
    api_key = 'NQCNSVTJWGI0E1IW'  # Consider keeping your API keys secure and not hard-coded
    stock_parameters = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': ticker,
        'apikey': api_key
    }

    try:
        stock_response = requests.get(stock_api_url, params=stock_parameters)
        stock_response.raise_for_status()  # Raises an HTTPError for bad responses
        stock_data = stock_response.json()
        daily_prices = stock_data.get('Time Series (Daily)')
        if daily_prices is None:
            raise ValueError("Time Series (Daily) data is not available in the response.")
        
        # Create DataFrame
        df = pd.DataFrame.from_dict(daily_prices, orient='index')
        df = df.astype({'1. open': 'float', '2. high': 'float', '3. low': 'float', '4. close': 'float', '5. volume': 'int'}).reset_index()
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'])
        df['Ticker'] = ticker
        df = df[['Date','Ticker', 'Volume', 'Open', 'High', 'Low', 'Close']]
        return df

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except ValueError as e:
        print(f"Data processing error: {e}")
        return pd.DataFrame()