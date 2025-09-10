import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load tasks.")
    return []

# Save tasks to file
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Update listbox with tasks
def update_listbox(task_list=None):
    listbox.delete(0, tk.END)
    if task_list is None:
        task_list = sorted(tasks, key=lambda x: x["done"])  # Show undone first
    for i, task in enumerate(task_list):
        status = "✅" if task["done"] else "❌"
        listbox.insert(tk.END, f"{status} {task['title']}")
        color = "gray" if task["done"] else "black"
        listbox.itemconfig(i, fg=color)

# Add new task
def add_task():
    title = entry.get().strip()
    if not title:
        messagebox.showwarning("Warning", "Task cannot be empty.")
        return
    if any(task["title"].lower() == title.lower() for task in tasks):
        messagebox.showwarning("Warning", "Task already exists.")
        return
    tasks.append({"title": title, "done": False})
    entry.delete(0, tk.END)
    update_listbox()
    save_tasks()

# Mark selected task as done
def mark_done():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "Select a task to mark done.")
        return
    index = selected[0]
    tasks[index]["done"] = True
    update_listbox()
    save_tasks()

# Delete selected task
def delete_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Info", "Select a task to delete.")
        return
    index = selected[0]
    del tasks[index]
    update_listbox()
    save_tasks()

# Search tasks
def search_task():
    keyword = search_entry.get().strip().lower()
    if not keyword:
        messagebox.showinfo("Info", "Enter a keyword to search.")
        return
    filtered = [task for task in tasks if keyword in task["title"].lower()]
    update_listbox(filtered)

# Show all tasks
def show_all():
    update_listbox()

# Toggle task done/undone on double-click
def toggle_done(event):
    selection = listbox.curselection()
    if not selection:
        return
    index = selection[0]
    tasks[index]["done"] = not tasks[index]["done"]
    update_listbox()
    save_tasks()

# ----------------- GUI SETUP -----------------

window = tk.Tk()
window.title("Simple Task Manager")
window.geometry("400x500")
window.resizable(False, False)

# Entry to add task
entry = tk.Entry(window, width=30)
entry.pack(pady=10)

add_btn = tk.Button(window, text="Add Task", command=add_task)
add_btn.pack()

# Frame for listbox and scrollbar
frame = tk.Frame(window)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, width=50, height=10, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)
scrollbar.config(command=listbox.yview)

listbox.bind("<Double-Button-1>", toggle_done)

# Buttons for done and delete
done_btn = tk.Button(window, text="Mark as Done", command=mark_done)
done_btn.pack(pady=5)

delete_btn = tk.Button(window, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

# Search section
search_label = tk.Label(window, text="Search Task")
search_label.pack(pady=(20, 5))

search_entry = tk.Entry(window, width=30)
search_entry.pack()

search_btn = tk.Button(window, text="Search", command=search_task)
search_btn.pack(pady=5)

show_all_btn = tk.Button(window, text="Show All", command=show_all)
show_all_btn.pack(pady=5)

# Load and show tasks
tasks = load_tasks()
update_listbox()

window.mainloop()
