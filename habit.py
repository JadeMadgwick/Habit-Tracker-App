from datetime import datetime, timedelta

from sympy import false


class Habit:
    """
    Represents a single habit.
    """

    def __init__(self, name: str, start_date: str, frequency: str, unit = None , target_value = None):
        """
        Initialize a habit.

              Args:
                  name (str): Name of the habit.
                  start_date (str): format date string 'YYYY-MM-DD'.
                  frequency (str): 'daily' or 'weekly'
                  unit (str): unit of habit: 'km', 'ml' , 'hours'
                  target_value (str): target value for the habit unit: '5'.
              """
        self.name = name
        self.start_date = datetime.fromisoformat(start_date)
        self.frequency = frequency.lower()
        self.unit = unit.lower() if unit else None
        self.target_value = target_value
        self.completed_dates = []  # List of ISO date strings
        self.streak = 0

    def mark_complete(self, date: str = None):
        """
              Mark the habit as completed on a given date.

              Args:
                  date (str): ISO date string to mark completion. Defaults to today.
              """
        if date is None:
            date = datetime.now().date().isoformat()
        if date not in self.completed_dates:
            self.completed_dates.append(date)
            self.update_streak()

    def update_streak(self):
        """
        Update the current streak based on completed_dates.
        """
        if not self.completed_dates:
            self.streak = 0
            return

        # Sort dates descending
        dates = sorted([datetime.fromisoformat(d).date() for d in self.completed_dates], reverse=True)

        streak_count = 1
        current = dates[0]

        for prev in dates[1:]:
            delta = (current - prev).days
            if self.frequency == 'daily':
                # Expect previous day to be one day before current
                if delta == 1:
                    streak_count += 1
                    current = prev
                else:
                    break
            elif self.frequency == 'weekly':
                # Expect previous week (7 days before current)
                if delta == 7:
                    streak_count += 1
                    current = prev
                else:
                    break
            else:
                break

        self.streak = streak_count

    def reset_streak(self):
        """
        Reset the current streak.
        """
        self.streak = 0

    def get_progress(self):
        """
        Returns a dict with total completions and current streak.
        """
        return {
            'total_completions': len(self.completed_dates),
            'streak': self.streak
        }

    def is_due(self, date=None) -> bool:
        """
        Check if the habit is due on the given date.
        Returns False if already completed.
        """
        if date is None:
            date_obj = datetime.now().date()
        elif isinstance(date, str):
            date_obj = datetime.fromisoformat(date).date()
        else:
            date_obj = date  # Already a date object

        # Check if it's already completed
        if date_obj.isoformat() in self.completed_dates:
            return False

        # DAILY habits
        if self.frequency == 'daily':
            return date_obj >= self.start_date.date()

        # WEEKLY habits (due every 7 days from start_date)
        elif self.frequency == 'weekly':
            delta = (date_obj - self.start_date.date()).days
            return delta >= 0 and delta % 7 == 0

        return False

    def to_dict(self):
        """
        Serialize habit to a dictionary for saving in JSON.
        """
        return {
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'frequency': self.frequency,
            'unit': self.unit,
            'target_value': self.target_value,
            'completed_dates': self.completed_dates,
            'streak': self.streak
        }

    @staticmethod
    def from_dict(data):
        """
        Deserialize habit from dictionary.
        """
        habit = Habit(data['name'], data['start_date'], data['frequency'], unit = data.get('unit'), target_value = data.get('target_value'))
        habit.completed_dates = data.get('completed_dates', [])
        habit.streak = data.get('streak', 0)
        return habit
