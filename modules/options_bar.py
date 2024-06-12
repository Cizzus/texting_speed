import tkinter as tk
from .records_page import RecordsPage


class OptionsBar:
    def __init__(self, root):
        menubar = tk.Menu()
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=file_menu, label="Options")

        file_menu.add_command(
            label="Records",
            command=lambda: root.show_frame(RecordsPage)
        )

        file_menu.add_command(
            label="Change player",
            command=lambda: root.show_instructions()
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=root.destroy
        )

        root.config(menu=menubar)
