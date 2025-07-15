# app_controller.py

from tracker import Tracker
from analytics import Analytics
from datetime import datetime

class AppController:
    """
    Main CLI app controller for the habit tracker.
    """

    def __init__(self):
        self.tracker = Tracker()
        self.analytics = Analytics(self.tracker)

    def run(self):
        """
               Run the main app loop.
               """
        while True:
            self.show_menu()
            choice = input("Choose an option ").strip()

            if choice == "1":
                self.create_habit()
            elif choice == "2":
                self.manage_habits()
            elif choice == "3":
                self.mark_habit_complete()
            elif choice == "4":
                self.view_analytics()
            elif choice.lower() in ("5", "q", "quit", "exit"):
                print("Exiting Habit Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    def show_menu(self):
        """
        Display the main menu.
        """
        print("\n====== HABIT TRACKER MENU ======")
        print("1. Create a new habit")
        print("2. Manage habits (view, edit, delete)")
        print("3. Mark habit as completed")
        print("4. View analytics")
        print("5. Quit")

    def create_habit(self):
        name = input("Enter habit name: ").strip()
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        frequency = input("Frequency (daily/weekly): ").strip().lower()

        if frequency not in ("daily", "weekly"):
            print("Invalid frequency. Must be 'daily' or 'weekly'.")
            return

        try:
            datetime.fromisoformat(start_date)
        except ValueError:
            print("Invalid date format.")
            return

        unit = input("Enter the unit you want to track (e.g km, ml, hours, etc.): ").strip().lower()
        target_value = input("Enter your goal to reach per day/week of your unit: ").strip().lower()

        # validate number

        try:
            target_value = float(target_value)
        except ValueError:
            print("Invalid target. Must be a number.")
            return

        print(f"\nReview your habit:")
        print(f"Name      : {name}")
        print(f"Start Date: {start_date}")
        print(f"Frequency : {frequency}")
        print(f"Unit      : {unit}")
        print(f"Target    : {target_value} {unit} {frequency}")

        save = input("Do you want to save this habit (y/n): ").strip().lower()
        if save == "y":
            success = self.tracker.add_habit(name, start_date, frequency, unit, target_value)
            if success:
                print(f"Habit '{name}' created successfully!")
            else:
                print(f"Habit '{name}' already exists.")
        elif save == "n":
            confirm = input("Are you sure you want to cancel this habit creation? (y/n): ").strip().lower()
            if confirm == "y":
                print("Your habit has been discarded.")
            elif confirm == "n":
                success = self.tracker.add_habit(name, start_date, frequency, unit, target_value)
                if success:
                    print(f"Habit '{name}' created successfully!")
                else:
                    print(f"Habit '{name}' already exists.")
        else:
            print("Invalid input. Habit not saved.")

    def manage_habits(self):
        """
        View all habits, and allow editing or deleting them.
        """
        habits = self.tracker.get_all_habits()

        if not habits:
            print("No habits to manage.")
            return

        print("\nYour Habits:")
        for i, habit in enumerate(habits, 1):
            print(f"{i}. {habit.name} ({habit.frequency})")

        choice = input("Enter habit name to edit/delete or press Enter to go back: ").strip()

        if choice in self.tracker.habits:
            action = input("Type 'edit' to edit or 'delete' to delete: ").strip().lower()

            if action == "edit":
                new_name = input("New name (leave blank to keep current): ").strip()
                new_start = input("New start date (YYYY-MM-DD or leave blank): ").strip()
                new_freq = input("New frequency (daily/weekly or leave blank): ").strip().lower()
                new_unit = input("New unit (leave blank to keep current): ").strip()
                new_target_value = input("New target value (leave blank to keep current): ").strip()

                self.tracker.edit_habit(
                    choice,
                    new_name if new_name else None,
                    new_start if new_start else None,
                    new_freq if new_freq else None,
                    new_unit if new_unit else None,
                    float(new_target_value) if new_target_value else None
                )

                print("Habit updated.")
            elif action == "delete":
                confirm_delete = input("Are you sure you want to delete this habit? (y/n)").strip().lower()
                if confirm_delete == ("y"):
                    self.tracker.delete_habit(choice)
                    print("Habit deleted.")
                elif confirm_delete == ("n"):
                    return
                else:
                    print("Invalid action.")
            else:
                print("Invalid action.")
        else:
            if choice:
                print("Habit not found.")

    def mark_habit_complete(self):
        """
        Let user check off habits due today.
        """
        today = datetime.now().date().isoformat()
        habits_due = self.tracker.get_today_habits(today)

        if not habits_due:
            print("No habits due today.")
            return

        print("\nHabits Due Today:")
        for i, habit in enumerate(habits_due, 1):
            print(f"{i}. {habit.name}")

        to_mark = input("Enter habit name to mark as complete (or press Enter to skip): ").strip()

        if to_mark in self.tracker.habits:
            self.tracker.mark_habit_complete(to_mark)
            print(f"Habit '{to_mark}' marked as complete.")
        else:
            print("Habit not found or not due today.")

    def view_analytics(self):
        """
        Display basic analytics to the user.
        """
        print("\n===== Habit Analytics =====")

        longest = self.analytics.get_longest_streak()
        if longest:
            print(f"📈 Longest streak: {longest} days")
        else:
            print("No habits to analyze.")

        struggled = self.analytics.get_struggled_habits()
        if struggled:
            print("\n💡 Habits with low streaks:")
            for habit in struggled:
                print(f"- {habit.name} (Streak: {habit.streak})")
        else:
            print("\nYou're doing great! No weak habits detected.")

        freq = input("\nType 'daily' or 'weekly' to see habits by frequency, or press Enter to skip: ").strip().lower()
        if freq in ("daily", "weekly"):
            filtered = self.analytics.get_habits_by_frequency(freq)
            print(f"\nHabits with frequency '{freq}':")
            for habit in filtered:
                print(f"- {habit.name} (Streak: {habit.streak})")




if __name__ == "__main__":
    app = AppController()
    app.run()


