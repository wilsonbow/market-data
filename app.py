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
            temp_label = Label(text=share, background_color=(0, 0, 1, 1))
            self.root.ids.books.add_widget(temp_label)


Stocks().run()
