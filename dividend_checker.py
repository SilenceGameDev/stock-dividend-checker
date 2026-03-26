import os

import requests
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")


@dataclass
class DividendChecker:
    pass

    def check_stock(self, ticker_symbol):
        # Get yesterday's closing stock price
        stock_params = {
            "function": "TIME_SERIES_WEEKLY_ADJUSTED",
            "symbol": ticker_symbol,
            "apikey": STOCK_API_KEY,
        }

        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        data = response.json()["Weekly Adjusted Time Series"]
        data_list = [value for (key, value) in data.items()]
        week_data = data_list[0]
        week_dividend_amount = week_data["7. dividend amount"]
        print(week_dividend_amount)

        # Get last week dividend amount
        last_week_data = data_list[1]
        last_week_dividend_amount = last_week_data["7. dividend amount"]
        print(last_week_dividend_amount)


