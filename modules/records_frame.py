import tkinter as tk
from sqlalchemy import desc
from .main_frame import MainFrame
from .database_config import session, Player, Result


class RecordsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollbar_frame = tk.Frame(self.canvas)
        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.config(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor='nw')
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Buttons
        switch_window_button = tk.Button(
            self,
            text="Go to the Main Screen",
            command=lambda: controller.show_frame(MainFrame),
        )
        refresh_button = tk.Button(
            self,
            text="Refresh",
            command=self._show_data
        )

        self._show_data()

        # Grid layout
        switch_window_button.pack(side="bottom", fill=tk.X)
        refresh_button.pack(side="bottom", fill=tk.X)
        self.canvas.pack(side="left", fill='both', expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _show_data(self):
        header = ["Player", "Words per minute", "Score"]
        for col_num, header in enumerate(header):
            label = tk.Label(self.scrollbar_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col_num, padx=10, pady=5)

        data = session.query(Player, Result).join(Result).order_by(desc(Result.words_per_minute),
                                                                   desc(Result.score)).all()

        for row_num, (player, result) in enumerate(data, start=1):
            row_data = [player.username, result.words_per_minute, result.score]
            for col_num, cell in enumerate(row_data):
                label = tk.Label(self.scrollbar_frame, text=cell, font=("Arial", 12))
                label.grid(row=row_num, column=col_num, padx=10, pady=5)
