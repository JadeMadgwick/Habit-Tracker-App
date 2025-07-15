# Habit Tracker App

This is a Python-based habit tracking application designed for individuals who want to build and monitor their daily or weekly habits. The app supports streak tracking, flexible frequency settings, and includes analytical features to help users build consistent routines over time.

---

## What is it?

This app allows users to:

- Create, edit, and delete habits
- Track progress for daily and weekly habits
- View current streaks and total completions
- Use time-series data to analyze habit consistency
- Automatically save and load habit data from JSON
- Run unit tests to verify correctness of core features

The project is built using Object-Oriented Programming and follows modular design principles. It was developed as part of a university programming course and includes all required documentation, test coverage, and a structured folder layout.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JadeMadgwick/Habit-Tracker-App
   
2. Install dependencies:

pip install -r requirements.txt

## Usage 

To Start the Application:
python App_Controller.py

And follow the instructions in the terminal to:

- Create new habits

- Edit and delete habits

- Mark habits as completed

- View your current progress and streaks

## Testing 

A full suite of unit tests is included and covers:

Habit creation, editing, and deletion

Streak logic for both daily and weekly habits

Filtering and frequency-based analytics

To run all tests, use:
pytest .


Tests are located in the test_project.py file and automatically generate simulated habit data for validation.

## Project Structure 

- `habit.py`: Defines the Habit class and its behavior
- `tracker.py`: Manages multiple habits, filtering, and persistence
- `analytics.py`: Calculates streaks and performance insights
- `App_Controller.py`: Command-line interface and main app logic
- `test_project.py`: Contains unit tests with 4 weeks of dummy data
- `data/habits.json`: Stores habit data automatically
- `README.md`: Project overview and usage instructions
- `requirements.txt`: Lists required Python packages
- `.gitignore`: Excludes unwanted files like `__pycache__/`
