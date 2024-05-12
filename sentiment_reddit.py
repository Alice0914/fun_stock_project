import requests
import pandas as pd
from datetime import datetime

# Define the function to fetch data
def fetch_data(date=None):
    url = 'https://tradestie.com/api/v1/apps/reddit'
    if date:
        url += f'?date={date}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['date'] = datetime.strptime(date, "%Y-%m-%d") if date else datetime.today().date()
    new_columns = ['No of Comments', 'Sentiment', 'Sentiment Score', 'Ticker', 'Date']
    if len(df.columns) == len(new_columns):
        df.columns = new_columns
    else:
        print("Column length mismatch:", df.columns)
    return df

