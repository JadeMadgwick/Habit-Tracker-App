from functools import reduce


class Analytics:
    """
    Provides habit analysis and statistics using data from Tracker.
    """

    def __init__(self, tracker):
        self.tracker = tracker

    def get_all_habits(self):
        """
        Return a list of all tracked habits.
        """
        return self.tracker.get_all_habits()

    def get_habits_by_frequency(self, frequency):
        return self.tracker.get_habits_by_frequency(frequency)

    def get_longest_streak(self):
        habits = self.tracker.get_all_habits()
        if not habits:
            return None

        return max(h.streak for h in habits)

    def get_longest_streak_for_habit(self, habit_name):
        """
        Return the longest streak for a specific habit.
        """
        habit = self.tracker.habits.get(habit_name)
        if habit:
            return habit.streak
        return None

    def get_struggled_habits(self):
        """
        Return habits with low completion (streak less than 2).
        """
        return [habit for habit in self.tracker.get_all_habits() if habit.streak < 2]