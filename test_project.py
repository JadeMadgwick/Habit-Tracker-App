import unittest
import os
import shutil
from tracker import Tracker
from habit import Habit
from datetime import datetime, timedelta

TEST_DATA_PATH = "data/habits.json"

class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        # Ensure fresh Tracker with clean test data
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)
        self.tracker = Tracker()

    def test_add_and_get_habit(self):
        self.tracker.add_habit("Exercise", "2025-06-01", "daily", "km", "5")
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].name, "Exercise")
        self.assertEqual(habits[0].unit, "km")
        self.assertEqual(habits[0].target_value, "5")

    def test_delete_habit(self):
        self.tracker.add_habit("Exercise", "2025-06-01", "daily")
        self.tracker.delete_habit("Exercise")
        self.assertEqual(len(self.tracker.get_all_habits()), 0)

    def test_edit_habit(self):
        self.tracker.add_habit("Exercise", "2025-06-01", "daily")
        self.tracker.edit_habit("Exercise", new_name="Gym", new_frequency="weekly")
        habit = self.tracker.get_all_habits()[0]
        self.assertEqual(habit.name, "Gym")
        self.assertEqual(habit.frequency, "weekly")

    def test_mark_habit_complete(self):
        self.tracker.add_habit("Meditate", "2025-06-01", "daily")
        self.tracker.mark_habit_complete("Meditate", "2025-06-10")
        habit = self.tracker.habits["Meditate"]
        self.assertIn("2025-06-10", habit.completed_dates)
        self.assertGreaterEqual(habit.streak, 1)

    def test_get_habits_by_frequency(self):
        self.tracker.add_habit("Exercise", "2025-06-01", "daily")
        self.tracker.add_habit("Read", "2025-06-01", "weekly")
        daily = self.tracker.get_habits_by_frequency("daily")
        self.assertEqual(len(daily), 1)
        self.assertEqual(daily[0].name, "Exercise")

    def test_streak_calculation_with_sample_data(self):
        self.tracker.add_habit("Exercise", "2025-06-01", "daily")
        habit = self.tracker.habits["Exercise"]

        # Simulate 4 days in a row of completions
        base_date = datetime(2025, 6, 10)
        for i in range(4):
            date_str = (base_date + timedelta(days=i)).date().isoformat()
            habit.mark_complete(date_str)

        habit.update_streak()
        self.assertEqual(habit.streak, 4)

    def test_weekly_streak_calculation(self):
        self.tracker.add_habit("Journal", "2025-06-01", "weekly")
        habit = self.tracker.habits["Journal"]

        base_date = datetime(2025, 6, 2)
        for i in range(4):
            date_str = (base_date + timedelta(weeks=i)).date().isoformat()
            habit.mark_complete(date_str)

        habit.update_streak()
        self.assertEqual(habit.streak, 4)

    def test_get_today_habits(self):
        self.tracker.add_habit("Exercise", datetime.today().date().isoformat(), "daily")
        today_habits = self.tracker.get_today_habits()
        self.assertGreaterEqual(len(today_habits), 1)
        self.assertEqual(today_habits[0].name, "Exercise")

    def tearDown(self):
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)

if __name__ == '__main__':
    unittest.main()

