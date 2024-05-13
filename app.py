import streamlit as st
from datetime import datetime
from sentiment_reddit import fetch_data
from data_loader import load_time_series_data
from TimeSeries_ML import (
    perform_analysis, plot_stock_data, forecast_stock_price,
    predicted_stock_price, predicted_value_graph, plot_trend_seasonality, 
    changePoint_graph, changePoint_date, model_error_metrics
)
from finance_data import (
    load_tickers, get_company_names, get_company_sector, get_company_revenueGrowth, 
    get_company_earningsGrowth, get_company_enterpriseValue
)

def load_css(file_path):
    # Load CSS file for styling.
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def setup_sidebar():
    # Set up sidebar for user inputs and return user choices.
    tickers = load_tickers() 
    ohlc_options = ['Open', 'High', 'Low', 'Close']
    tickers_with_default = ["Select Option"] + tickers
    
    ticker = st.sidebar.selectbox("Select a ticker symbol:", tickers_with_default, index=0)
    OHLC = st.sidebar.selectbox("Select OHLC value for analysis:", ohlc_options)
    predicted_days = st.sidebar.number_input("Enter number of days to predict:", min_value=1, max_value=10, value=7, step=1)
    date_input = st.sidebar.date_input("Select the date for Sentiment Analysis Data:", datetime.today())
    return ticker, OHLC, predicted_days, date_input
        
def display_header():
    # Display the main header for the dashboard.
    st.markdown(f"<h1 style='font-size:38px;'>WallStreetBets Big Board: Top 50 Stockss</h1>", unsafe_allow_html=True)

def handle_ticker_selection(ticker):
    # Display ticker selection details.
    if ticker != "Select Option":
        col1, col2 = st.columns(2)
        #col1, col_div, col2 = st.columns([1,0.1,1])
        
        with col1:
            st.write(f"You selected <br><span class='large-font'>**{ticker}**</span>", unsafe_allow_html=True)
            st.write(f"Company Name <br><span class='large-font'>**{get_company_names(ticker)}**</span>", unsafe_allow_html=True)
            st.write(f"Sector <br><span class='large-font'>**{get_company_sector(ticker)}**</span>", unsafe_allow_html=True)
        #with col_div:
            #st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with col2:
            st.write(f"Earnings Growth <br><span class='large-font'>**{get_company_earningsGrowth(ticker)}**</span>", unsafe_allow_html=True) 
            st.write(f"Revenue Growth <br><span class='large-font'>**{get_company_revenueGrowth(ticker)}**</span>", unsafe_allow_html=True)  
            st.write(f"Enterprise Value <br><span class='large-font'>**{get_company_enterpriseValue(ticker)}**</span>", unsafe_allow_html=True) 
    else:
        st.write("Please select a ticker symbol from the dropdown.")

def perform_data_analysis(ticker, OHLC, predicted_days, date_input):
    # Load data, perform analysis, and display results.
    formatted_date = date_input.strftime("%Y-%m-%d")
    df = load_time_series_data(ticker)
    sentiment_df = fetch_data(formatted_date)

    if not df.empty:
        display_stock_analysis(df, ticker, OHLC)
        display_stock_predictions(df, ticker, OHLC, predicted_days)
        display_changePoint_analysis(df, ticker, OHLC, predicted_days)
        display_model_error_metrics(df, ticker, OHLC)
        display_sentiment_analysis(sentiment_df, ticker, formatted_date)
    else:
        st.error("Failed to fetch time series data or no data available for this ticker.")

def display_stock_analysis(df, ticker, OHLC):
    # Display stock analysis and plots.
    st.subheader(f"{ticker} {OHLC} Price Analysis: A 100-Day Overview") 
    analysis = perform_analysis(df)
    st.dataframe(analysis, width=1200)

    st.subheader(f"Visualizing the Stock Data for {ticker} - {OHLC} Price")
    st.pyplot(plot_stock_data(df, OHLC))

def display_stock_predictions(df, ticker, OHLC, predicted_days):
    # Display stock predictions and trend analysis.
    st.subheader(f"Predicted Stock Prices for {ticker} - Next {predicted_days} Days")
    pred_values = predicted_stock_price(df, OHLC, predicted_days)
    st.dataframe(pred_values, width=1200)
    st.pyplot(predicted_value_graph(df, OHLC, predicted_days))

    model, forecast = forecast_stock_price(df, OHLC, predicted_days)
    st.subheader(f"Trend and Seasonality for {ticker} - {OHLC} Price")
    fig = plot_trend_seasonality(model, forecast)
    st.pyplot(fig)

def display_changePoint_analysis(df, ticker, OHLC, predicted_days):
     # Plot the vertical lines where the potential changepoints occurred and display changepoints date.
    model, forecast = forecast_stock_price(df, OHLC, predicted_days)
    st.subheader(f"{ticker} {OHLC} Price Change Point in Past 100 Business Days")
    fig = changePoint_graph(model, forecast)
    st.pyplot(fig)
    
    st.subheader(f"{ticker} {OHLC} Price Change Point Date") 
    changepoints_analysis = changePoint_date(model)
    st.dataframe(changepoints_analysis, width=1200)

def display_model_error_metrics(df, ticker, OHLC):
    metrics_result = model_error_metrics(df, OHLC)
    st.subheader(f"{ticker} {OHLC} Model Error Metrics")
    st.dataframe(metrics_result, width=1200)

def display_sentiment_analysis(sentiment_df, ticker, date):
    # Display sentiment analysis data.
    if not sentiment_df.empty:
        sentiment_df = sentiment_df[sentiment_df['Ticker'] == ticker]
        if not sentiment_df.empty:
            sentiment_df.reset_index(drop=True, inplace=True)
            st.subheader(f"Sentiment Data for {ticker} on {date}")
            #html = sentiment_df.to_html(index=False)
            #st.markdown(html, unsafe_allow_html=True)
            st.dataframe(sentiment_df, width=1200)
        else:
            st.warning(f"No sentiment data found for {ticker} on {date}")
    else:
        st.error("Failed to fetch sentiment data or no data available for this date.")

def main():
    load_css("style.css")
    ticker, OHLC, predicted_days, date_input = setup_sidebar()  
    display_header()
    handle_ticker_selection(ticker)
    
    if st.sidebar.button("Load Data and Analyze"):
        perform_data_analysis(ticker, OHLC, predicted_days, date_input)

if __name__ == "__main__":
    main()