import yfinance as yf
import pandas as pd

def load_tickers():
    tickers = pd.read_csv('tickers.csv')
    return tickers['ticker'].tolist()

def get_company_names(ticker):
    ticker_data = yf.Ticker(ticker).info
    name = ticker_data.get('longName', 'Unknown Company')
    return name

def get_company_sector(ticker):
    ticker_data = yf.Ticker(ticker).info
    sector = ticker_data.get('sector', 'Unknown Company')
    return sector

def get_company_revenueGrowth(ticker):
    ticker_data = yf.Ticker(ticker).info
    revenueGrowth = ticker_data.get('revenueGrowth', 'Unknown Company')
    return revenueGrowth

def get_company_earningsGrowth(ticker):
    ticker_data = yf.Ticker(ticker).info
    earningsGrowth = ticker_data.get('earningsGrowth', 'Unknown Company')
    return earningsGrowth

def get_company_enterpriseValue(ticker):
    ticker_data = yf.Ticker(ticker).info
    enterpriseValue = ticker_data.get('enterpriseValue', 'Unknown Company')
    return enterpriseValue



