# WallStreetBets Big Board: Top 50 Stocks Application

## Project Description
**WallStreetBets Big Board: Top 50 Stocks Application** offers insightful and interactive stock analysis for the 50 most discussed stocks on Reddit's WallStreetBets. Utilizing the modern time series forecasting tool, **Prophet**, developed by Meta, this application provides predictions of stock prices for the next 10 days.

### Key Features
- **Financial Information Display**: Shows real-time data fetched from legal APIs.
- **Descriptive Statistical Analysis**: Offers trend analysis and identifies significant change points in stock prices over the past 100 days.
- **Predictive Analysis**: Forecasts stock prices for up to 10 days ahead.
- **Sentiment Analysis**: Analyzes sentiments based on comments from Reddit's WallStreetBets.

[Watch the Video](https://youtu.be/Ux_QUVPsueA)

### Data Sources
Data is retrieved from:
- [Alpha Vantage](https://www.alphavantage.co/)
- [Tradestie](https://tradestie.com/)

Both sources are accessed using published API keys, compliant with legal permissions.

## Repository Structure
- `data_loader.py`: Handles API requests to load data.
- `TimeSeries_ML.py`: Manages the training of the model and generates predictions.
- `sentiment_reddit.py`: Fetches sentiment scores based on Reddit data.
- `finance_data.py`: Generates financial data using the yfinance library.
- `app.py`: Integrates and displays all data in a Streamlit web application.
- `style.css`: Contains CSS styles for the project.
- `tickers.csv`: Lists the top 50 stocks discussed on Reddit's WallStreetBets.
- `.dockerignore`: Specifies untracked files that Docker should ignore.
- `Docker-compose.yml`: Configures services, networks, and volumes for Docker.
- `Dockerfile`: Instructions for building the Docker image.
- `requirements.txt`: Lists all Python packages required for the project.

## Build Instructions
### Building the Docker Image
To build the Docker image, run the following command in the project directory:
```commandline
docker build -t my_streamlit_app:v1.0 .
```

## Run Instructions:
### Running the App
To run the app, execute:
```commandline
docker run -p 8501:8501 my_streamlit_app:v1.0
```

Then, open your web browser and go to **http://localhost:8501** to view the app.