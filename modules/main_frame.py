import os
import random
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
from fuzzywuzzy import fuzz
from .database_config import Player, Result, session


class MainFrame(tk.Frame):
    FINISH_TIME = 0.0
    TIME_LEFT = 60.0
    START_COUNTER = 5
    FONT_SIZE = 15

    def __init__(self, parent, controller):
        super().__init__(parent)
        # Timer
        self.finish_time = self.FINISH_TIME
        # Seconds left until test end
        self.time_left_s = self.TIME_LEFT
        # Seconds left before start
        self.start_counter_s = self.START_COUNTER

        # This variable inherits main window (main.py) attributes and methods.
        self.controller = controller

        # Labels
        label = tk.Label(self, text="Test Your Texting Speed!", font=("arial", 20))
        # Function takes a random text from the media/stories directory
        self.text = self.__text_to_write()
        # Text to show before test start
        self.text_label = tk.Label(self, text="Text will be shown here!", font=("arial", 15))
        # Time label to track time of the test.
        self.seconds_label = tk.Label(self, text=f"Time left: {self.time_left_s} s", font=("arial", 15))

        # Text window where user type
        self.text_window = tk.Text(self, font=("arial", 15), state=tk.DISABLED)

        # Buttons
        self.start_button = tk.Button(self, text="Start", width=20, command=self._start_time)

        # Image of reset button
        image = Image.open("./media/reset.png")
        image.thumbnail(size=(20, 20))
        self.photo = ImageTk.PhotoImage(image)

        self.reset_button = tk.Button(self, text="Reset", image=self.photo, command=self._reset_time)

        # Grid layout
        label.grid_configure(column=0, row=0, columnspan=2)
        self.text_label.grid_configure(column=0, row=1, columnspan=2)
        self.text_window.grid_configure(column=0, row=2, padx=10, pady=10, columnspan=2)
        self.start_button.grid_configure(column=0, row=3, pady=10, sticky="e")
        self.reset_button.grid_configure(column=1, row=3, sticky="w")
        self.seconds_label.grid_configure(column=1, row=4, pady=10, sticky="e", padx=20)

    def _start_time(self):
        """
        Function starts the test when user clicks the 'Start' button.
        """
        self.start_button.config(text="Stop", command=self._stop_time)
        # While tes time is running 'Reset' button is disabled.
        self.reset_button.config(state=tk.DISABLED)
        # Starts the counter until test start
        self.__start_counter()

    def _stop_time(self):
        """
        Function stops the test when user clicks the 'Stop' button.
        """
        # Changes given story text into given 'text' string while test is stopped
        self.text_label.config(text="Text will be shown here!", font=('Arial', self.FONT_SIZE))
        # Typing is disabled while test stopped
        self.text_window.config(state=tk.DISABLED)
        # Time finish_time is changed to time left of the test to stop the clock (look at '_update_time' function)
        self.finish_time = self.time_left_s

        # Enable 'Reset' button
        self.reset_button.config(state=tk.ACTIVE)
        # 'Stop' button renamed to 'Resume' and command '_resume_time' added.
        self.start_button.config(text="Resume", command=self._resume_time)

    def _resume_time(self):
        """
        Function resumes the test when user clicks 'Resume' after stopping the test.
        """
        # Given story text is loaded into label for user to rewrite.
        self.text_label.config(text=self.text, font=('Arial', self.FONT_SIZE))
        # Enable user to type into text typing window.
        self.text_window.config(state=tk.NORMAL)
        # Time finish_time reset to time when test must be finished (FINISH_TIME: 0.0)
        self.finish_time = self.FINISH_TIME
        # Reset button is disabled when test run.
        self.reset_button.config(state=tk.DISABLED)
        # Function follow how much time left until the end of the test.
        self.__update_time()
        # 'Resume' button is renamed to 'Stop' and _stop_time functionality is given as a command.
        self.start_button.config(text="Stop", command=self._stop_time)

    def _reset_time(self):
        # Reset start counter time to original. (Default: START_COUNTER = 5)
        self.start_counter_s = self.START_COUNTER
        # If the test is finished due to the time finish_time 'start_button' is disabled. So after 'Reset' start_button is enabled.
        self.start_button.config(state=tk.ACTIVE)
        # This part deletes user text in the text typing window.
        self.text_window.config(state=tk.NORMAL)
        self.text_window.delete("1.0", "end")
        self.text_window.config(state=tk.DISABLED)
        # Reset time to the starting conditions. (Default: TIME_LEFT=60)
        self.time_left_s = self.TIME_LEFT
        # Resetting finish time to its default value. This prevents program from crashing when user click 'Stop' and
        # then 'Reset'
        self.finish_time = self.FINISH_TIME
        # Reset clock label to the starting conditions.
        self.seconds_label.configure(text=f"Time left: {self.time_left_s} s", font=("arial", 15))
        # start_button is reconfigured to its starting conditions.
        self.start_button.config(text="Start", command=self._start_time)
        # New random story text is taken.
        self.text = self.__text_to_write()

    def __update_time(self):
        """
        Function tracks the timing of the test.
        """
        self.time_left_s -= 0.1
        if self.time_left_s > self.finish_time:
            seconds_left = round(self.time_left_s, 1)
            self.seconds_label.configure(text=f"Time left: {seconds_left} s")
            self.after(100, self.__update_time)

        # When user runs out of time (Finish test).
        elif round(self.time_left_s, 1) == 0.0:
            # GUI part.
            self.text_label.config(text="Text will be shown here!", font=('arial', self.FONT_SIZE))
            self.text_window.config(state=tk.DISABLED)
            self.seconds_label.configure(text="Time left: 0.0 s")
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.ACTIVE)

            # Data part where results are taken and saved.
            speed, score = self._result()
            player_db = session.query(Player).filter_by(username=self.controller.USERNAME).first()
            result = Result(player_id=player_db.id_, words_per_minute=speed, score=score)
            session.add(result)
            session.commit()

    def __start_counter(self):
        """
        Function counts the seconds left until start.
        """
        self.text_window.config(state=tk.NORMAL)
        self.text_window.delete("1.0", "end")
        custom_font = font.Font(family="Arial", size=60)
        self.text_window.tag_config("custom_font", font=custom_font, justify="center")
        self.text_window.insert(tk.END, f"{self.start_counter_s}", "custom_font")
        self.start_counter_s -= 1
        if self.start_counter_s >= 0:
            self.after(1000, self.__start_counter)
        else:
            self.text_window.delete("1.0", "end")
            self.text_label.config(text=self.text, font=('Arial', self.FONT_SIZE))
            self.__update_time()

    @staticmethod
    def __text_to_write() -> str:
        """
        Function takes a random story from media/stories dictionary and returns it as a string.
        This string is loaded into label as the text that user will rewrite during the test.
        """
        stories = os.listdir("./media/stories")
        story_to_write = random.choice(stories)
        with open(f"./media/stories/{story_to_write}", "r") as f:
            text = f.read()

        return text

    def _result(self) -> tuple:
        """
        Function takes the user given text and compares it with the original to count the Levenshtein distance and
        count how many of words per minte the user types.
        """
        text = self.text_window.get("1.0", "end")
        words_per_min = len(text.split())
        score = fuzz.ratio(self.text, text)
        player = self.controller.USERNAME
        message = f"{player} result:\nWords per minute: {int(words_per_min)}\nLevenshtein distance (score): {score}"
        messagebox.showinfo("Result", message)
        return words_per_min, score
