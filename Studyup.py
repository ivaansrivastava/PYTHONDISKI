import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
from threading import Thread

# Base directory for storing notes
BASE_DIR = "StudyUP"

# Ensure the base directory exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Function to update the subject dropdown
def update_subject_dropdown():
    selected_class = class_var.get()
    class_dir = os.path.join(BASE_DIR, selected_class)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
        # Add default subjects
        for subject in ["English", "Maths"]:
            subject_dir = os.path.join(class_dir, subject)
            if not os.path.exists(subject_dir):
                os.makedirs(subject_dir)
    subjects = os.listdir(class_dir)
    subjects.append("Add Subject...")  # Add the "Add Subject..." option
    subject_dropdown["values"] = subjects
    if subjects:
        subject_var.set(subjects[0])
        update_chapter_dropdown()
    else:
        subject_var.set("")
        chapter_dropdown["values"] = []
        chapter_var.set("")
        notes_text.delete("1.0", tk.END)

# Function to update the chapter dropdown
def update_chapter_dropdown():
    selected_class = class_var.get()
    selected_subject = subject_var.get()
    if not selected_class or not selected_subject or selected_subject == "Add Subject...":
        chapter_dropdown["values"] = []
        chapter_var.set("")
        notes_text.delete("1.0", tk.END)
        return
    subject_dir = os.path.join(BASE_DIR, selected_class, selected_subject)
    chapters = os.listdir(subject_dir)
    chapters.append("Add Chapter...")  # Add the "Add Chapter..." option
    chapter_dropdown["values"] = chapters
    if chapters:
        chapter_var.set(chapters[0])
        load_notes()
    else:
        chapter_var.set("")
        notes_text.delete("1.0", tk.END)

# Function to load notes for the selected chapter
def load_notes():
    selected_class = class_var.get()
    selected_subject = subject_var.get()
    selected_chapter = chapter_var.get()
    if not selected_class or not selected_subject or not selected_chapter or selected_chapter == "Add Chapter...":
        notes_text.delete("1.0", tk.END)
        return
    notes_file = os.path.join(BASE_DIR, selected_class, selected_subject, selected_chapter, "notes.txt")
    if os.path.exists(notes_file):
        with open(notes_file, "r") as f:
            notes_text.delete("1.0", tk.END)
            notes_text.insert("1.0", f.read())
    else:
        notes_text.delete("1.0", tk.END)

# Function to save notes for the selected chapter
def save_notes():
    selected_class = class_var.get()
    selected_subject = subject_var.get()
    selected_chapter = chapter_var.get()
    if not selected_class or not selected_subject or not selected_chapter or selected_chapter == "Add Chapter...":
        messagebox.showwarning("Warning", "Please select a class, subject, and chapter!")
        return
    chapter_dir = os.path.join(BASE_DIR, selected_class, selected_subject, selected_chapter)
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)
    notes_file = os.path.join(chapter_dir, "notes.txt")
    with open(notes_file, "w") as f:
        f.write(notes_text.get("1.0", tk.END).strip())
    messagebox.showinfo("Success", "Notes saved successfully!")

# Function to add a new subject
def add_subject():
    selected_class = class_var.get()
    if not selected_class:
        messagebox.showwarning("Warning", "Please select a class!")
        return
    new_subject = simpledialog.askstring("Add Subject", "Enter the new subject name:")
    if new_subject:
        class_dir = os.path.join(BASE_DIR, selected_class)
        subject_dir = os.path.join(class_dir, new_subject)
        if not os.path.exists(subject_dir):
            os.makedirs(subject_dir)
            update_subject_dropdown()
            messagebox.showinfo("Success", f"Subject '{new_subject}' added successfully!")
        else:
            messagebox.showwarning("Warning", f"Subject '{new_subject}' already exists!")

# Function to add a new chapter
def add_chapter():
    selected_class = class_var.get()
    selected_subject = subject_var.get()
    if not selected_class or not selected_subject or selected_subject == "Add Subject...":
        messagebox.showwarning("Warning", "Please select a class and subject!")
        return
    new_chapter = simpledialog.askstring("Add Chapter", "Enter the new chapter name:")
    if new_chapter:
        chapter_dir = os.path.join(BASE_DIR, selected_class, selected_subject, new_chapter)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
            update_chapter_dropdown()
            messagebox.showinfo("Success", f"Chapter '{new_chapter}' added successfully!")
        else:
            messagebox.showwarning("Warning", f"Chapter '{new_chapter}' already exists!")

# Pomodoro Timer
def start_pomodoro():
    try:
        work_time = int(work_time_entry.get()) * 60
        break_time = int(break_time_entry.get()) * 60
    except ValueError:
        messagebox.showwarning("Warning", "Please enter valid numbers for work and break times!")
        return

    def run_timer():
        for remaining in range(work_time, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            timer_label.config(text=f"Work: {minutes:02}:{seconds:02}")
            time.sleep(1)
        messagebox.showinfo("Break Time!", "Time for a break!")
        for remaining in range(break_time, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            timer_label.config(text=f"Break: {minutes:02}:{seconds:02}")
            time.sleep(1)
        messagebox.showinfo("Pomodoro Complete!", "Great job! Pomodoro session complete.")
        timer_label.config(text="")

    Thread(target=run_timer, daemon=True).start()

# Create the main Tkinter window
root = tk.Tk()
root.title("StudyUP")
root.geometry("900x600")

# Sidebar Frame
sidebar_frame = tk.Frame(root, width=250, bg="lightgray")
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Class Selection
class_label = tk.Label(sidebar_frame, text="Select Class:", bg="lightgray", font=("Helvetica", 12))
class_label.pack(pady=5)
class_var = tk.StringVar()
class_dropdown = ttk.Combobox(sidebar_frame, textvariable=class_var, font=("Helvetica", 12))
class_dropdown["values"] = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "College"]
class_dropdown.pack(pady=5)
class_dropdown.bind("<<ComboboxSelected>>", lambda e: update_subject_dropdown())

# Subject Selection
subject_label = tk.Label(sidebar_frame, text="Select Subject:", bg="lightgray", font=("Helvetica", 12))
subject_label.pack(pady=5)
subject_var = tk.StringVar()
subject_dropdown = ttk.Combobox(sidebar_frame, textvariable=subject_var, font=("Helvetica", 12))
subject_dropdown.pack(pady=5)
subject_dropdown.bind("<<ComboboxSelected>>", lambda e: (add_subject() if subject_var.get() == "Add Subject..." else update_chapter_dropdown()))

# Chapter Selection
chapter_label = tk.Label(sidebar_frame, text="Select Chapter:", bg="lightgray", font=("Helvetica", 12))
chapter_label.pack(pady=5)
chapter_var = tk.StringVar()
chapter_dropdown = ttk.Combobox(sidebar_frame, textvariable=chapter_var, font=("Helvetica", 12))
chapter_dropdown.pack(pady=5)
chapter_dropdown.bind("<<ComboboxSelected>>", lambda e: (add_chapter() if chapter_var.get() == "Add Chapter..." else load_notes()))

# Pomodoro Timer
pomodoro_label = tk.Label(sidebar_frame, text="Pomodoro Timer", bg="lightgray", font=("Helvetica", 14, "bold"))
pomodoro_label.pack(pady=10)

work_time_label = tk.Label(sidebar_frame, text="Work Time (min):", bg="lightgray", font=("Helvetica", 12))
work_time_label.pack(pady=5)
work_time_entry = tk.Entry(sidebar_frame, font=("Helvetica", 12), width=10)
work_time_entry.pack(pady=5)

break_time_label = tk.Label(sidebar_frame, text="Break Time (min):", bg="lightgray", font=("Helvetica", 12))
break_time_label.pack(pady=5)
break_time_entry = tk.Entry(sidebar_frame, font=("Helvetica", 12), width=10)
break_time_entry.pack(pady=5)

start_pomodoro_button = tk.Button(sidebar_frame, text="Start Pomodoro", font=("Helvetica", 12), command=start_pomodoro)
start_pomodoro_button.pack(pady=10)

timer_label = tk.Label(sidebar_frame, text="", bg="lightgray", font=("Helvetica", 12))
timer_label.pack(pady=10)

# Notes Editor
notes_frame = tk.Frame(root)
notes_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

notes_label = tk.Label(notes_frame, text="Notes Editor", font=("Helvetica", 14, "bold"))
notes_label.pack(pady=10)

notes_text = tk.Text(notes_frame, font=("Helvetica", 12), wrap=tk.WORD)
notes_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

save_button = tk.Button(notes_frame, text="Save Notes", font=("Helvetica", 12), command=save_notes)
save_button.pack(pady=10)

# Initialize the dropdowns
class_var.set("Class 1")
update_subject_dropdown()

# Run the Tkinter event loop
root.mainloop()