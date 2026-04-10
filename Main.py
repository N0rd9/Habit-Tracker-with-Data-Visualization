import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DATA_FILE = "habits.json"

# -------------------- Data Handling --------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f, indent=4)

habits = load_data()

# -------------------- Habit Logic --------------------

def add_habit():
    name = simpledialog.askstring("Add Habit", "Habit name:")
    if name and name not in habits:
        habits[name] = []
        save_data()
        update_listbox()

def mark_completed():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a habit first.")
        return

    habit = listbox.get(selection[0])
    today = datetime.now().strftime("%Y-%m-%d")

    if today not in habits[habit]:
        habits[habit].append(today)
        save_data()
        update_listbox()
        messagebox.showinfo("Success", f"Marked '{habit}' as completed today!")
    else:
        messagebox.showinfo("Info", "Habit already completed today.")

def calculate_streak(dates):
    if not dates:
        return 0

    dates = sorted(datetime.strptime(d, "%Y-%m-%d") for d in dates)
    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            streak += 1
            max_streak = max(max_streak, streak)
        elif dates[i] != dates[i - 1]:
            streak = 1

    return max_streak

def update_listbox():
    listbox.delete(0, tk.END)
    for habit, dates in habits.items():
        streak = calculate_streak(dates)
        listbox.insert(tk.END, f"{habit} (🔥 {streak} days)")

# -------------------- Visualization --------------------

def show_statistics():
    if not habits:
        messagebox.showinfo("Info", "No habits to display.")
        return

    names = []
    counts = []

    for habit, dates in habits.items():
        names.append(habit)
        counts.append(len(dates))

    plt.figure()
    plt.bar(names, counts)
    plt.title("Habit Completion Counts")
    plt.xlabel("Habits")
    plt.ylabel("Days Completed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# -------------------- Export Data --------------------

def export_data():
    export_file = "habit_export.csv"
    with open(export_file, "w") as f:
        f.write("Habit,Date\n")
        for habit, dates in habits.items():
            for date in dates:
                f.write(f"{habit},{date}\n")
    messagebox.showinfo("Export", f"Data exported to {export_file}")

# -------------------- GUI Setup --------------------

root = tk.Tk()
root.title("Habit Tracker")
root.geometry("400x450")

title = tk.Label(root, text="Habit Tracker", font=("Arial", 18, "bold"))
title.pack(pady=10)

listbox = tk.Listbox(root, width=40, height=12)
listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Habit", width=15, command=add_habit).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Mark Completed", width=15, command=mark_completed).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Show Statistics", width=15, command=show_statistics).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Export Data", width=15, command=export_data).grid(row=1, column=1, padx=5, pady=5)

update_listbox()
root.mainloop()
