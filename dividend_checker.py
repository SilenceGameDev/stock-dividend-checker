import os
from datetime import datetime as dt
import requests
from dataclasses import dataclass
from dotenv import load_dotenv

from logger import logger

load_dotenv()

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")


@dataclass
class DividendChecker:
    pass

    def get_dividend_dictionary(self, ticker_symbol) -> list|str:
        stock_params = {
            "function": "TIME_SERIES_MONTHLY_ADJUSTED",
            "symbol": ticker_symbol,
            "apikey": STOCK_API_KEY,
        }
        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        response.raise_for_status()
        try:
            data = response.json()["Monthly Adjusted Time Series"]
        except KeyError:
            logger.info("Could not find ticker symbol")
            return ""
        # Getting the dividend amount for each month and adding it to a dictionary IF that value is > 0
        dividend_dict = [
            {
                # formatting the month/year to Month Year. Sorry to my non US peeps :(
                "month": dt.strptime(month, "%Y-%m-%d").strftime("%B %Y"),
                "dividend": float(values["7. dividend amount"])
            }
            for month, values in data.items()
            if float(values["7. dividend amount"]) > 0
        ]
        logger.info("Set dividend dictionary")
        return dividend_dict


