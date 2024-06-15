import tkinter as tk
from modules.options_bar import OptionsBar
from modules.main_frame import MainFrame
from modules.records_frame import RecordsFrame
from modules.welcome_window import WelcomeWindow


class Windows(tk.Tk):
    """
    Main window class that inherits tkinter.Tk object methods and attributes. This is the main program window
    which holds frames, option bars and welcome window objects.
    """
    USERNAME = "Unknown"

    def __init__(self, menubar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initiates welcome window where user input for username required
        self.welcome_window = WelcomeWindow(self)
        # Menu bar for more options initiated
        menubar(self)

        self.wm_title("Typing Speed Test")

        # Initiate main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to append main page and records page frames
        self.frames = {}

        for frame in (MainFrame, RecordsFrame):
            # Create frame instance from frame object
            new_frame = frame(container, self)

            # Saving different frame objects as a key and respectively frame instance object as a value.
            self.frames[frame] = new_frame
            new_frame.grid(row=0, column=0)

        # Show main frame when program starts
        self.show_frame(MainFrame)

    def show_frame(self, cont):
        """
        Function changes frame view.
        cont: tk.Frame object.
        """
        frame = self.frames[cont]
        frame.tkraise()

    def show_instructions(self):
        """
        Function initiates welcome window when called. This window contains instructions and user input to provide
        username.
        """
        WelcomeWindow(self)


# Initiates program
if __name__ == "__main__":
    testObj = Windows(OptionsBar)
    testObj.mainloop()
