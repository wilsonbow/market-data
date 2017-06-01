from kivy.app import App
from kivy.lang import Builder
from watchlist import Watchlist
from kivy.uix.label import Label


class Stocks(App):
    def __init__(self):
        super().__init__()
        self.build()
        self.my_watchlist = Watchlist()

    def build(self):
        self.title = 'Stock Watcher'
        self.root = Builder.load_file('app.kv')
        return self.root

    def update_list(self):
        self.root.ids.watchlist.clear_widgets()

        for share in self.my_watchlist.shares_dict:
            # Create button based on current share iteration
            price = self.my_watchlist.shares_dict[share].last_price
            temp_label = Label(text=share + '\n$' + price)
            self.root.ids.watchlist.add_widget(temp_label)

    def add_to_list(self):
        ticker = self.root.ids.code.text.upper()
        self.root.ids.statusbar.text = 'Added {} to list'.format(ticker)
        self.my_watchlist.add_share(ticker)
        self.update_list()
        self.root.ids.code.text = ""


Stocks().run()
