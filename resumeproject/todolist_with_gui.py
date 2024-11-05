import tkinter as tk
from tkinter import messagebox, font, ttk
from datetime import datetime
import ttkbootstrap as tb  # Modern theming library
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER, WARNING
from PIL import Image, ImageTk
import winsound

# Create the main application window with a themed style
app = tb.Window(themename="superhero")
app.title("To Do List")
app.geometry("500x600")

tasks = []


# Custom Tooltip Class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="lightyellow", relief="solid", borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# Function to play a sound on certain actions
def play_sound(action):
    sound_map = {
        "add": "SystemHand",
        "complete": "SystemAsterisk",
        "delete": "SystemExclamation"
    }
    winsound.PlaySound(sound_map.get(action), winsound.SND_ALIAS)


# Function to add a task with a due date and time
def add_task():
    task_text = task_entry.get()
    month_day_str = due_date_entry.get()
    time_str = due_time_entry.get()
    current_year = datetime.now().year

    try:
        due_date = datetime.strptime(f"{current_year}-{month_day_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showwarning("Date/Time Error", "Enter date in MM-DD and time in HH:MM format.")
        return

    if task_text:
        tasks.append({"task": task_text, "due_date": due_date, "completed": False})
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        due_time_entry.delete(0, tk.END)
        list_tasks()
        play_sound("add")
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")


# Function to list tasks, with overdue or completed highlighting
def list_tasks():
    task_listbox.delete(*task_listbox.get_children())
    sorted_tasks = sorted(tasks, key=lambda x: x["due_date"])
    now = datetime.now()

    for index, task in enumerate(sorted_tasks, start=1):
        due_date_str = task["due_date"].strftime("%m-%d %H:%M")
        completed_str = "✓" if task["completed"] else ""

        color = ""
        if task["completed"]:
            color = SUCCESS
        elif task["due_date"] < now:
            color = DANGER
        elif (task["due_date"] - now).days < 1:
            color = WARNING
        else:
            color = PRIMARY

        task_listbox.insert("", tk.END, iid=index, values=(task["task"], due_date_str, completed_str), tags=(color,))
    for tag in [PRIMARY, SUCCESS, DANGER, WARNING]:
        task_listbox.tag_configure(tag, foreground=app.style.colors.get(tag))


# Function to delete a selected task
def delete_task():
    selected_task = task_listbox.selection()
    if selected_task:
        task_index = int(selected_task[0]) - 1
        removed_task = tasks.pop(task_index)
        messagebox.showinfo("Task Deleted", f"'{removed_task['task']}' has been deleted.")
        list_tasks()
        play_sound("delete")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")


# Function to mark task as completed
def complete_task():
    selected_task = task_listbox.selection()
    if selected_task:
        task_index = int(selected_task[0]) - 1
        tasks[task_index]["completed"] = not tasks[task_index]["completed"]
        list_tasks()
        play_sound("complete")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")


# Label and Entry for Task
task_entry_label = tb.Label(app, text="Enter a new task:", bootstyle=PRIMARY)
task_entry_label.pack(pady=(10, 0))
task_entry = ttk.Entry(app, width=30)
task_entry.pack(pady=5)

# Date and Time Entries
due_date_label = tb.Label(app, text="Due date (MM-DD):", bootstyle=PRIMARY)
due_date_label.pack(pady=(5, 0))
due_date_entry = ttk.Entry(app, width=15)
due_date_entry.pack(pady=5)

due_time_label = tb.Label(app, text="Due time (HH:MM):", bootstyle=PRIMARY)
due_time_label.pack(pady=(5, 0))
due_time_entry = ttk.Entry(app, width=15)
due_time_entry.pack(pady=5)

# Buttons with tooltips and icons
add_task_button = tb.Button(app, text="Add Task", command=add_task, bootstyle=SUCCESS)
add_task_button.pack(pady=(10, 5))
ToolTip(add_task_button, "Add a new task with due date and time.")

complete_task_button = tb.Button(app, text="Mark as Completed", command=complete_task, bootstyle=PRIMARY)
complete_task_button.pack(pady=(5, 5))
ToolTip(complete_task_button, "Toggle task completion status.")

delete_task_button = tb.Button(app, text="Delete Task", command=delete_task, bootstyle=DANGER)
delete_task_button.pack(pady=(5, 10))
ToolTip(delete_task_button, "Delete the selected task.")

# Treeview for Task List with scrollbars
task_listbox = ttk.Treeview(app, columns=("Task", "Due Date", "✓"), show="headings", height=10)
task_listbox.heading("Task", text="Task")
task_listbox.heading("Due Date", text="Due Date")
task_listbox.heading("✓", text="✓")
task_listbox.pack(pady=10, padx=10, fill=tk.X)

scrollbar_y = ttk.Scrollbar(app, orient="vertical", command=task_listbox.yview)
task_listbox.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side="right", fill="y")

# Initial listing of tasks
list_tasks()

# Run the application
app.mainloop()
