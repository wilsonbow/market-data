"""
Share2 is a modified version of the Share class in the yahoo_finance module.
It also incorporates a last_price attribute extracted from googlefinance module
"""

from yahoo_finance import Share
from googlefinance import getQuotes
from urllib.error import HTTPError
from yahoo_finance import YQLResponseMalformedError


class Share2(Share):
    def __init__(self, code):
        super().__init__(code + '.AX')
        self.code = code
        self.last_price = None
        self.update_price()

    def __str__(self):
        return "{}: ${}".format(self.code, self.last_price)

    def __repr__(self):
        return "${}".format(self.last_price)

    def update_price(self):
        try:
            price = getQuotes('ASX:' + self.code)[0]['LastTradePrice']
            self.last_price = price
        except HTTPError:
            self.last_price = 0.00

    def get_price(self):
        return self.last_price
