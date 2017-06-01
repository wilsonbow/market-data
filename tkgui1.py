import tkinter


class Application(tkinter.Frame):

    def __init__(self, master=None):

        tkinter.Frame.__init__(self, master)

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.quitLabel = tkinter.Label(self, text='Quit')

        self.quitLabel.grid()


app = Application()

app.master.title('Sample application')

app.mainloop()
