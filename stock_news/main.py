import json
import os
from os.path import dirname, join
from typing import Any

import pandas
import requests
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)


class StockNews:
    def __init__(self, stock: str, alpha_key: str, news_api_key: str):
        self.stock = stock
        self.alpha_key = alpha_key
        self.news_api_key = news_api_key
        self.news_api = os.environ.get("NEWS_API")
        self.alpha_api = os.environ.get("ALPHA_API")

    def alpha_parameters(self) -> dict:
        alpha_parameters = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.stock,
            "interval": "60min",
            "apikey": self.alpha_key,
        }
        return alpha_parameters

    def request_alpha(self) -> Any:
        alpha = requests.get(self.alpha_api, params=self.alpha_parameters())  # type: ignore
        # print(alpha.raise_for_status())
        return alpha.json()

    def news_parameters(self) -> dict:
        new_parameters = {
            "q": self.stock,
            "sortBy": "popularity",
            "apiKey": self.news_api_key,
        }
        return new_parameters

    def request_new(self) -> Any:
        new = requests.get(self.news_api, params=self.news_parameters())  # type: ignore
        return new.json()

    def to_csv(self) -> None:
        data_alpha = pandas.DataFrame(self.request_alpha())
        with open("new.csv", "w") as txt:
            txt.write(data_alpha.to_csv())


def main():
    instance = StockNews(
        "TSLA", os.environ.get("ALPHA_KEY"), os.environ.get("NEWS_API_KEY")
    )
    with open("test.json", "w") as file:
        json.dump(instance.request_new(), file, indent=4)


if __name__ == "__main__":
    main()
