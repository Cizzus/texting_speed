
# Texting Speed Test Application

This project is a Texting Speed Test application built with Python, Tkinter for the GUI, and SQLAlchemy for database interaction. The application allows users to create a username, track their typing speed, and store the results in a MySQL database.

## Features

- User can create a username to track their records.
- The main page displays instructions for the typing test.
- The typing test starts with a 5-second countdown.
- A typing challenge where the user needs to rewrite the given text as fast as possible within 60 seconds.
- The results, including words per minute, are stored in a MySQL database.

## Prerequisites

- Python 3.x
- MySQL database
- Required Python packages

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Cizzus/texting_speed.git
   cd texting_speed
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database:**
   - Create a new MySQL database.
   - Update the `database_url` in the script `media/database_config.py` to match your MySQL credentials.

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Application Flow:**
   - Read the instruction and enter your username. Click "Submit"
   - Click "Start" to begin the typing test.
   - Type the given text as fast as you can within 60 seconds.
   - Your words per minute will be calculated and stored in the database.

## Project Structure

- `main.py`: Main application script.
- `modules`: Main parts of the application.
- `requirements.txt`: List of required Python packages.
- `README.md`: Project documentation.

## Example Code

### SQLAlchemy Models

```python
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

database_url = 'sqlite:///your_db.db'
engine = create_engine(database_url)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = 'players_table'
    id_ = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    results = relationship("Result", back_populates="player")

class Result(Base):
    __tablename__ = 'results'
    id_ = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players_table.id_"))
    words_per_minute = Column(Integer)
    player = relationship("Player", back_populates="results")

Base.metadata.create_all(engine)
```

### Tkinter GUI

```python
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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [MySQL](https://www.mysql.com/)
