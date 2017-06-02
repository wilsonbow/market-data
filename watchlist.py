"""
Watchlist class for use with BEAFS ASX app
"""

from share2 import Share2
from share2 import RetrievalError
import csv


class Watchlist:

    def __init__(self):
        self.shares_dict = {}

    def __str__(self):
        keys = ''
        for key in self.shares_dict:
            keys += ', {}: ${}'.format(key, self.shares_dict[key].last_price)
        keys = keys.lstrip(', ')
        return keys

    def __repr__(self):
        keys = ''
        for key in self.shares_dict:
            keys += ', {}'.format(key)
        keys = keys.lstrip(', ')
        return keys

    def update_details(self, code):
        self.remove_share(code)
        self.add_share(code)

    def add_share(self, code):
        if code in self.shares_dict:
            return None
        else:
            try:
                self.shares_dict[code] = Share2(code)
            except RetrievalError:
                return None

    def remove_share(self, code):
        try:
            self.shares_dict.pop(code)
        except KeyError:
            return None

    def update_prices(self):
        for key in self.shares_dict:
            self.shares_dict[key].update_price()

    def save_watchlist(self, file_name):
        with open(file_name, 'w', newline='') as fileID:
            data_writer = csv.writer(fileID)
            for key in self.shares_dict:
                data_writer.writerow([key])

    def load_watchlist(self, file_name):
        with open(file_name, 'r') as fileID:
            loaded_data = csv.reader(fileID)

            for row in loaded_data:
                self.add_share(row[0])
