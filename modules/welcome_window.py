import re
import tkinter as tk
from tkinter import messagebox
from .database_config import Player, session


class WelcomeWindow(tk.Toplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=300, height=200)
        self.title("Instructions Window")
        self.instructions_text_str = self.instructions_text()

        self.text_label = tk.Label(self, text=self.instructions_text_str, font=("arial", 16))
        self.username_label = tk.Label(self, text="Enter username: ", font=("arial", 16, "bold"))
        self.username_entry = tk.Entry(self, font=("arial", 16))

        self.submit_username = tk.Button(self, text="Submit", font=("arial", 14, "bold"), command=self._submit_username)

        # Protects window from closing on click.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Protects from starting the test with opened WelcomeWindow.
        self.grab_set()
        self.transient(root)

        self.text_label.grid_configure(column=0, row=0, pady=20, padx=20)
        self.username_label.grid_configure(column=0, row=1)
        self.username_entry.grid_configure(column=0, row=2)
        self.submit_username.grid_configure(column=0, row=3, pady=10)

        self.main_window = root

    def _submit_username(self):
        """
        Function checks if the provided username is correct due to the given rules (consist of letters and number,
        length 3<len(username)<30). Also, if the username do not exist in the database, it is added.
        """
        username = self.username_entry.get()
        if re.match(r"^[a-zA-Z0-9]*$", username) and (len(username) <= 30 & len(username) > 3):
            if session.query(Player).filter_by(username=username).first():
                self.main_window.USERNAME = username
                self.destroy()
            else:
                self.main_window.USERNAME = username
                user = Player(username=username)
                session.add(user)
                session.commit()
                self.destroy()
        else:
            messagebox.showwarning("Incorrect Username", "Provide username only with letters and numbers.\n"
                                                         "Username length must be longer than 3 and shorter than 30 characters.")

    @staticmethod
    def on_closing():
        # Override the close button to prevent closing the window
        messagebox.showwarning("Input Required", "Please enter some text before proceeding.")

    @staticmethod
    def instructions_text() -> str:
        """
        Returns instructions for the test. Instructions are taken from media/instructions.txt
        """
        with open("./media/instructions.txt", "r") as f:
            file = f.read()

        return file
