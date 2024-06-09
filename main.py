# Importing the tkinter module
import tkinter as tk
from modules.options_bar import OptionsBar
from modules.main_page import MainPage
from modules.records_page import RecordsPage


class Windows(tk.Tk):
    def __init__(self, menubar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title("Test Application")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar(self)

        self.frames = {}

        for F in (MainPage, RecordsPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    testObj = Windows(OptionsBar)
    testObj.mainloop()
