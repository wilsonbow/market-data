from kivy.app import App
from kivy.lang import Builder
from watchlist import Watchlist
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from threading import Timer
from yahoo_finance import YQLResponseMalformedError
from urllib.error import HTTPError


class Stocks(App):
    def __init__(self):
        super().__init__()
        self.build()
        self.my_watchlist = Watchlist()
        self.my_watchlist_name = "default_watchlist"
        self.update_timer = Timer(20, self.timer_cb)
        self.add_code_input = TextInput()
        self.add_watchlist_input = TextInput()

    def build(self):
        self.title = 'Stock Watcher'
        self.root = Builder.load_file('app.kv')
        return self.root

    def stop(self):
        self.my_watchlist.save_watchlist('{}.csv'.format(self.my_watchlist_name))

    # noinspection PyBroadException
    def load_watchlist(self, this_watchlist):
        self.my_watchlist.save_watchlist('{}.csv'.format(self.my_watchlist_name))
        self.my_watchlist = Watchlist()
        try:
            self.my_watchlist.load_watchlist('{}.csv'.format(this_watchlist.text))
            self.my_watchlist_name = this_watchlist.text
            self.update_list()
            self.update_statusbar('{} successfully loaded'.format(self.my_watchlist_name))
            self.update_timer = Timer(20, self.timer_cb)
            self.update_timer.start()
        except:
            self.update_statusbar('{} failed to load'.format(this_watchlist.text))

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

    def add_to_list(self, this_btn):
        ticker = self.add_code_input.text.upper()
        self.root.ids.statusbar.text = 'Added {} to list'.format(ticker)
        self.my_watchlist.add_share(ticker)
        self.update_list()
        self.add_code_input.text = ""

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

    def add_to_watchlist_menu(self):
        self.root.ids.menu.clear_widgets()
        self.root.ids.menu.add_widget(Label(text='Add share to\nwatchlist',
                                            color=(1, 0, 0, 1)))
        self.root.ids.menu.add_widget(self.add_code_input)
        temp_button = Button(text='Add to list')
        temp_button.bind(on_release=self.add_to_list)
        self.root.ids.menu.add_widget(temp_button)

    def choose_watchlist_menu(self):
        self.root.ids.menu.clear_widgets()
        self.root.ids.menu.add_widget(Label(text='Add\nwatchlist'))
        self.root.ids.menu.add_widget(self.add_watchlist_input)
        self.root.ids.menu.add_widget(Button(text='Add watchlist'))
        self.root.ids.menu.add_widget(Label(text='Choose\nwatchlist'))
        with open('watchlists.txt') as fileID:
            saved_watchlists = fileID.read().split('\n')
            for wl in saved_watchlists:
                temp_btn = Button(text=wl)
                temp_btn.bind(on_release=self.load_watchlist)
                self.root.ids.menu.add_widget(temp_btn)


Stocks().run()
