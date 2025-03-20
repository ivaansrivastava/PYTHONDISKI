# COPYRIGHT BY IVAAN (github.com/leaperstuff)
# MIT License
# FREE TO USE

# import libs
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Main window
root = tk.Tk()
root.title("Notes")
root.geometry("400x400")

# Text area
text = tk.Text(root, wrap="word")
text.pack(expand=True, fill="both")

# Navbar
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            text.delete("1.0", tk.END)
            text.insert(tk.END, file.read())
def save_file():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END))
def about():
    messagebox.showinfo("About", "This is a simple notes app")
navbar = tk.Menu(root)
root.config(menu=navbar)
file_menu = tk.Menu(navbar, tearoff=False)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
navbar.add_cascade(label="File", menu=file_menu)
navbar.add_command(label="About", command=about)
navbar.add_command(label="Exit", command=root.quit)

# Run the main loop
root.mainloop()
# This is a simple notes app. It has a text area where you can write notes. It also has a navbar with options to open, save, and exit. The notes are saved as plain text files. You can also display an about message.
# Run the main.py file and choose the Notes option to run the notes app. You can write notes, save them, and open existing notes files. You can also exit the app from the navbar.