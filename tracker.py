import json
import os
from habit import Habit

DATA_PATH = "data/habits.json"


class Tracker:
    """
    Manages all habits and handles data persistence.
    """

    def __init__(self):
        self.habits = {}  # key = habit name, value = Habit instance
        self.load_habits()

    def add_habit(self, name, start_date, frequency, unit=None, target_value=None):
        if name in self.habits:
            return False  # habit already exists

        new_habit = Habit(name, start_date, frequency, unit, target_value)
        self.habits[name] = new_habit
        self.save_habits()
        return True

    def delete_habit(self, name):
        """
        Delete a habit by name.
        """
        if name in self.habits:
            del self.habits[name]
            self.save_habits()
        else:
            print("Habit not found.")

    def edit_habit(self, name, new_name=None, new_start_date=None, new_frequency=None):
        if name not in self.habits:
            print("Habit not found.")
            return

        habit = self.habits[name]
        if new_name:
            habit.name = new_name
            self.habits[new_name] = habit
            del self.habits[name]
        if new_start_date:
            habit.start_date = new_start_date
        if new_frequency:
            habit.frequency = new_frequency.lower()
        self.save_habits()

    def mark_habit_complete(self, name, date=None):
        """
        Mark a specific habit as complete for a given date.
        """
        if name in self.habits:
            self.habits[name].mark_complete(date)
            self.save_habits()
        else:
            print("Habit not found.")

    def get_all_habits(self):
        """
        Return a list of all habits.
        """
        return list(self.habits.values())

    def get_habits_by_frequency(self, frequency):
        """
        Return habits that match a given frequency (daily/weekly).
        """
        return [habit for habit in self.habits.values() if habit.frequency == frequency.lower()]

    def get_today_habits(self, date=None):
        """
        Return habits due today (based on frequency).
        """
        today_habits = []
        for habit in self.habits.values():
            if habit.is_due(date):
                today_habits.append(habit)
        return today_habits

    def save_habits(self):
        """
        Save habits to a JSON file.
        """
        os.makedirs("data", exist_ok=True)
        data = [habit.to_dict() for habit in self.habits.values()]
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def load_habits(self):
        """
        Load habits from a JSON file.
        """
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r") as f:
                data = json.load(f)
                for habit_data in data:
                    habit = Habit.from_dict(habit_data)
                    self.habits[habit.name] = habit