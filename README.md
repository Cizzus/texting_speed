
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

database_url = 'mysql+mysqlconnector://your_username:your_password@your_host/your_database'
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
from tkinter import Frame, Label, Scrollbar, Canvas

def create_gui(data):
    root = tk.Tk()
    root.title("SQLAlchemy Joined Tables in Tkinter")

    frame = Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')

    canvas = Canvas(frame)
    canvas.grid(row=0, column=0, sticky='nsew')

    scrollbar = Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Configure the main window to adjust with resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Add table headers
    headers = ["Player ID", "Username", "Created At", "Result ID", "Words Per Minute"]
    for col_num, header in enumerate(headers):
        label = Label(scrollable_frame, text=header, font=('Arial', 12, 'bold'))
        label.grid(row=0, column=col_num, padx=10, pady=5, sticky='nsew')

    # Add table data
    for row_num, (player, result) in enumerate(data, start=1):
        row_data = [player.id_, player.username, player.created_at, result.id_, result.words_per_minute]
        for col_num, cell in enumerate(row_data):
            label = Label(scrollable_frame, text=cell, font=('Arial', 12))
            label.grid(row=row_num, column=col_num, padx=10, pady=5, sticky='nsew')

    # Configure columns to expand
    for i in range(len(headers)):
        scrollable_frame.grid_columnconfigure(i, weight=1)

    root.mainloop()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [MySQL](https://www.mysql.com/)
