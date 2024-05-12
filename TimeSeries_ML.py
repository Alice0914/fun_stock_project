import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation, performance_metrics
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import mean_squared_error, mean_absolute_error
from data_loader import load_time_series_data
    
##################  Summary of dataset  ##################
def perform_analysis(df):
    df_price = df[['Open', 'High', 'Low', 'Close']]
    return df_price.describe()

##################  Visualize the data  ##################
def plot_stock_data(df, OHLC):
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Define color palette
    colors = {OHLC: '#1f77b4', 'Volume': '#7f7f7f'}

    # Plot price data
    ax1.plot(df['Date'], df[OHLC], label=OHLC, color=colors[OHLC], marker='o', linestyle='-', linewidth=2)

    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('Price', fontsize=14)
    ax1.legend(loc='upper left', fontsize=12)

    # Create a secondary y-axis for volume
    ax2 = ax1.twinx()
    width = 1  # Set width to 1 by default, adjust as needed based on your date intervals
    if len(df['Date']) > 1:
        width = (df['Date'].iloc[1] - df['Date'].iloc[0]).days
    ax2.bar(df['Date'], df['Volume'], label='Volume', color=colors['Volume'], alpha=0.3, width=width)
    ax2.set_ylabel('Volume', fontsize=14)
    ax2.legend(loc='upper right', fontsize=12)

    # Format date on x-axis
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.grid(True, linestyle='--', linewidth='0.5', color='grey')
    ax1.set_xlim([df['Date'].min(), df['Date'].max()])

    # Title including the range of dates
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    end_date = df['Date'].max().strftime('%Y-%m-%d')
    plt.title(f'Stock Prices and Volume Over Time: {start_date} ~ {end_date}', fontsize=16)

    plt.gcf().autofmt_xdate()  # Rotate date labels to fit them better
    plt.tight_layout()
    return fig
    
##################  Time Series Forecasting with Prophet  ##################
### OHLC = ['Open', 'High', 'Low', 'Close']
def model_stock_price(df, OHLC, predicted_days):
    df = df[['Date', OHLC]].rename(columns={'Date': 'ds', OHLC: 'y'})
    model = Prophet()
    model.fit(df)
    return model

def forecast_stock_price(df, OHLC, predicted_days):
    #Make Future Predictions
    model = model_stock_price(df, OHLC, predicted_days)
    future_dates = model.make_future_dataframe(periods=predicted_days, freq='B')  # 'B' to continue excluding weekends
    forecast = model.predict(future_dates)
    return model, forecast

def predicted_stock_price(df, OHLC, predicted_days):
    #Extract the last 10 days (days=10) of predictions from the forecast dataframe
    model, forecast  = forecast_stock_price(df, OHLC, predicted_days)
    predicted_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(predicted_days)
    predicted_values.columns = ['Date', 'Predicted Value', 'Predicted Lower Bound', 'Predicted Upper Bound']
    return predicted_values

##################  output1: table - Predicted value from model ##################
def predicted_value_table(df, OHLC, predicted_days):
    pred_value_df = predicted_stock_price(df, OHLC, predicted_days)
    return pred_value_df

##################  output2: graph - Predicted value from model ##################
def predicted_value_graph(df, OHLC, predicted_days):
    model = model_stock_price(df, OHLC, predicted_days)
    model, forecast = forecast_stock_price(df, OHLC, predicted_days)
    fig = model.plot(forecast, figsize=(10, 6))
    ax = fig.gca()
    
    max_date = df['Date'].max()  
    predicted_part = forecast[forecast['ds'] > max_date]

    # Highlight the prediction period
    ax.fill_between(predicted_part['ds'], predicted_part['yhat_lower'], predicted_part['yhat_upper'], color='#FF6666', alpha=0.5)

    # Add annotations for the start and end dates of the prediction
    start_date = predicted_part['ds'].min()
    end_date = predicted_part['ds'].max()
    ax.annotate(f'Start: {start_date.date()}', xy=(start_date, predicted_part.iloc[0]['yhat']),
                xytext=(start_date, predicted_part.iloc[0]['yhat'] + (ax.get_ylim()[1] - ax.get_ylim()[0]) / 10),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='left', verticalalignment='top')
    
    ax.annotate(f'End: {end_date.date()}', xy=(end_date, predicted_part.iloc[-1]['yhat']),
                xytext=(end_date, predicted_part.iloc[-1]['yhat'] - (ax.get_ylim()[1] - ax.get_ylim()[0]) / 10),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='bottom')

    ax.set_title('Forecast with Prediction Highlighted', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel(f'{OHLC} Values', fontsize=14)
    ax.legend(['Historical Data', 'Predicted Trend', 'Confidence Interval'])

    return fig
##################  output3: graph - Plot the trend and seasonality ##################
def plot_trend_seasonality(model, forecast):
    fig = model.plot_components(forecast)
    plt.tight_layout()  
    return fig

##################  output4: graph-Adding ChangePoints to Prophet  ##################  
#plot the vertical lines where the potential changepoints occurred
def changePoint_graph(model, forecast):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig = model.plot(forecast, ax=ax)
    add_changepoints_to_plot(ax, model, forecast)
    plt.tight_layout()
    return fig

def changePoint_date(model):
    return model.changepoints
##################  Calculate Error Metrics  ################## 
# forecasting accuracy is generally measured by error metrics
# Split into train and test
def model_error_metrics(df, OHLC, predicted_days):
    df = df[['Date', OHLC]].rename(columns={'Date': 'ds', OHLC: 'y'})
    train = df.iloc[:80]
    test = df.iloc[80:]

    model, forecast = forecast_stock_price(df, OHLC, predicted_days)

    y_pred = forecast['yhat'].tail(predicted_days).values
    y_true = test['y'].values

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    metrics_df = pd.DataFrame({
        'Metric': ['MAE', 'MSE', 'RMSE', 'MAPE'],
        'Value': [mae, mse, rmse, mape]
    })

    return metrics_df
