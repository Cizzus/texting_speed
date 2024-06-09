import tkinter as tk
from PIL import Image, ImageTk
from fuzzywuzzy import fuzz
from .instructions import instructions


class MainPage(tk.Frame):
    TIME_LIMIT = 0.0
    START_TIME = 60.0
    INSTRUCTIONS = instructions

    def __init__(self, parent, controller):
        super().__init__(parent)
        # Timer
        self.limit = self.TIME_LIMIT
        self.seconds = self.START_TIME

        image = Image.open("./media/reset.png")
        image.thumbnail(size=(20, 20))
        self.photo = ImageTk.PhotoImage(image)

        # Labels
        label = tk.Label(self, text="Test Your Texting Speed!", font=("arial", 20))
        self.text = self.text_to_write()
        self.text_label = tk.Label(self, text=self.INSTRUCTIONS, font=("arial", 10))
        self.seconds_label = tk.Label(self, text=f"Time left: {self.seconds} s", font=("arial", 15))

        # Text window
        self.text_window = tk.Text(self, font=("arial", 15), state=tk.DISABLED)

        # Buttons
        self.start_button = tk.Button(self, text="Start", width=20, command=self.start_time)
        self.reset_button = tk.Button(self, text="Reset", image=self.photo, command=self.reset_time)

        # Grid layout
        label.grid_configure(column=0, row=0, columnspan=2)
        self.text_label.grid_configure(column=0, row=1, columnspan=2)
        self.text_window.grid_configure(column=0, row=2, padx=10, pady=10, columnspan=2)
        self.start_button.grid_configure(column=0, row=3, pady=10, sticky="e")
        self.reset_button.grid_configure(column=1, row=3, sticky="w")
        self.seconds_label.grid_configure(column=1, row=4, pady=10, sticky="e", padx=20)

    def start_time(self):
        self.text_label.config(text=self.text)
        self.text_window.config(state=tk.NORMAL)
        self.update_time()
        self.start_button.config(text="Stop", command=self.stop_time)
        self.reset_button.config(state=tk.DISABLED)

    def stop_time(self):
        self.text_label.config(text=self.INSTRUCTIONS)
        self.text_window.config(state=tk.DISABLED)
        self.limit = self.seconds

        self.reset_button.config(state=tk.ACTIVE)
        self.start_button.config(text="Resume", command=self.resume_time)

    def resume_time(self):
        self.text_label.config(text=self.text)
        self.text_window.config(state=tk.NORMAL)
        self.limit = self.TIME_LIMIT
        self.reset_button.config(state=tk.DISABLED)
        self.update_time()
        self.start_button.config(text="Stop", command=self.stop_time)

    def reset_time(self):
        self.start_button.config(state=tk.ACTIVE)
        self.text_window.config(state=tk.NORMAL)
        self.text_window.delete("1.0", "end")
        self.text_window.config(state=tk.DISABLED)
        self.seconds = self.START_TIME
        self.limit = self.TIME_LIMIT
        self.seconds_label.configure(text=f"Time left: {self.seconds} s", font=("arial", 15))
        self.start_button.config(text="Start", command=self.start_time)

    def update_time(self):
        self.seconds -= 0.1
        if self.seconds > self.limit:
            seconds_left = round(self.seconds, 1)
            self.seconds_label.configure(text=f"Time left: {seconds_left} s")
            self.after(10, self.update_time)

        elif round(self.seconds, 1) == 0.0:
            self.text_label.config(text=self.INSTRUCTIONS)
            text = self.text_window.get("1.0", "end")
            words_per_min = len(text.split())
            score = fuzz.ratio(self.text, text)
            print(f"Words per minute: {int(words_per_min)}\nLevenshtein distance (score): {score}")
            self.text_window.config(state=tk.DISABLED)
            self.seconds_label.configure(text="0.0")
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.ACTIVE)

    @staticmethod
    def text_to_write() -> str:
        with open("./text.txt", "r") as f:
            text = f.read()

        return text
