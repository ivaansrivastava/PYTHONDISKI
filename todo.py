# To-Do List App with Tkinter GUI
# COPYRIGHT By IVAAN (github.com/ivaansrivastava)
# MIT License

import os
import tkinter as tk
from tkinter import messagebox

# File to store tasks
TODO_FILE = "todo.txt"

# Function to load tasks from the file
def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Function to save tasks to the file
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        file.writelines([task + "\n" for task in tasks])

# Function to update the task list display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Function to add a new task
def add_task():
    new_task = task_entry.get().strip()
    if new_task:
        tasks.append(new_task)
        save_tasks(tasks)
        update_task_list()
        task_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Task added successfully!")
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to delete a selected task
def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = tasks.pop(selected_task_index[0])
        save_tasks(tasks)
        update_task_list()
        messagebox.showinfo("Success", f"Task '{task}' deleted successfully!")
    else:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# Function to exit the app
def exit_app():
    root.destroy()

# Load tasks from the file
tasks = load_tasks()

# Create the main Tkinter window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")

# Title Label
title_label = tk.Label(root, text="To-Do List", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Task Listbox
task_listbox = tk.Listbox(root, font=("Helvetica", 12), height=15, width=40, selectmode=tk.SINGLE)
task_listbox.pack(pady=10)
update_task_list()

# Task Entry
task_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
task_entry.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", font=("Helvetica", 12), command=add_task)
add_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete Task", font=("Helvetica", 12), command=delete_task)
delete_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 12), command=exit_app)
exit_button.grid(row=0, column=2, padx=5)

# Run the Tkinter event loop
root.mainloop()