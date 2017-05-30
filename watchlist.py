"""
Watchlist class for use with BEAFS ASX app
"""

from share2 import Share2


class Watchlist:

    def __init__(self):
        self.shares_dict = {}

    def __str__(self):
        keys = ''
        for key in self.shares_dict:
            keys += ', {}'.format(key)
        keys = keys.lstrip(', ')
        return keys

    def __repr__(self):
        return self.__str__()

    def update_details(self, code):
        self.remove_share(code)
        self.add_share(code)

    def add_share(self, code):
        if code in self.shares_dict:
            return None
        else:
            self.shares_dict[code] = Share2(code)

    def remove_share(self, code):
        try:
            self.shares_dict.pop(code)
        except KeyError:
            return None
