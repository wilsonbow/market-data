from kivy.app import App
from kivy.lang import Builder
from watchlist import Watchlist
from kivy.uix.label import Label
from threading import Timer
from yahoo_finance import YQLResponseMalformedError
from urllib.error import HTTPError


class Stocks(App):
    def __init__(self):
        super().__init__()
        self.build()
        self.my_watchlist = Watchlist()
        self.update_timer = Timer(20, self.timer_cb)

    def build(self):
        self.title = 'Stock Watcher'
        self.root = Builder.load_file('app.kv')
        return self.root

    def stop(self):
        self.my_watchlist.save_watchlist('my_watchlist.csv')

    # noinspection PyBroadException
    def load_watchlist(self):
        try:
            self.my_watchlist.load_watchlist('my_watchlist.csv')
            self.update_list()
            self.update_statusbar('Watchlist successfully loaded')
            self.update_timer.start()
        except:
            self.update_statusbar('Watchlist failed to load')

    def update_list(self):
        self.root.ids.watchlist.clear_widgets()

        for share in self.my_watchlist.shares_dict:
            # Create button based on current share iteration
            price = self.my_watchlist.shares_dict[share].last_price
            try:
                temp_label = Label(text=share + '\n$' + price,
                                   font_size=24)
                self.root.ids.watchlist.add_widget(temp_label)
            except TypeError:
                pass

    def add_to_list(self):
        ticker = self.root.ids.code.text.upper()
        self.root.ids.statusbar.text = 'Added {} to list'.format(ticker)
        self.my_watchlist.add_share(ticker)
        self.update_list()
        self.root.ids.code.text = ""

    def update_prices(self):
        self.root.ids.add_share_btn.state = 'down'
        self.my_watchlist.update_prices()
        self.update_list()
        self.update_statusbar('Prices successfully updated!')
        self.root.ids.add_share_btn.state = 'normal'

    def update_statusbar(self, message):
        self.root.ids.statusbar.text = message

    # noinspection PyBroadException
    def timer_cb(self):
        self.update_timer.cancel()
        self.update_statusbar('Updating current stock prices...')
        try:
            self.update_prices()
        except:
            pass
        self.update_timer = Timer(20, self.timer_cb)
        self.update_timer.start()


Stocks().run()
