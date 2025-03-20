# COPYRIGHT By IVAAN (github.com/ivaansrivastava)
# MIT License
# FREE TO USE

# import libs
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Ensure the notes directory exists
NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

class NoteEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Editor")
        
        # Sidebar for notes
        self.sidebar = tk.Frame(root, width=200, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.note_listbox = tk.Listbox(self.sidebar)
        self.note_listbox.pack(fill=tk.BOTH, expand=True)
        self.note_listbox.bind("<<ListboxSelect>>", self.load_note)
        
        # Buttons for note operations
        self.new_button = tk.Button(self.sidebar, text="New Note", command=self.new_note)
        self.new_button.pack(fill=tk.X)
        
        self.delete_button = tk.Button(self.sidebar, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(fill=tk.X)
        
        self.rename_button = tk.Button(self.sidebar, text="Rename Note", command=self.rename_note)
        self.rename_button.pack(fill=tk.X)
        
        self.move_button = tk.Button(self.sidebar, text="Move Note", command=self.move_note)
        self.move_button.pack(fill=tk.X)
        
        self.new_folder_button = tk.Button(self.sidebar, text="New Folder", command=self.new_folder)
        self.new_folder_button.pack(fill=tk.X)
        
        # Text editor for notes
        self.text_editor = tk.Text(root)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        self.current_note = None
        self.load_notes()
    
    def load_notes(self):
        self.note_listbox.delete(0, tk.END)
        for root_dir, dirs, files in os.walk(NOTES_DIR):
            for file in files:
                if file.endswith(".txt"):
                    relative_path = os.path.relpath(os.path.join(root_dir, file), NOTES_DIR)
                    self.note_listbox.insert(tk.END, relative_path)
    
    def load_note(self, event):
        selection = self.note_listbox.curselection()
        if not selection:
            return
        note_path = os.path.join(NOTES_DIR, self.note_listbox.get(selection[0]))
        with open(note_path, "r") as file:
            content = file.read()
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, content)
        self.current_note = note_path
    
    def save_current_note_content(self):
        if self.current_note:
            with open(self.current_note, "w") as file:
                file.write(self.text_editor.get(1.0, tk.END).strip())
    
    def new_note(self):
        self.save_current_note_content()
        note_name = simpledialog.askstring("New Note", "Enter note name:")
        if note_name:
            note_path = os.path.join(NOTES_DIR, note_name + ".txt")
            with open(note_path, "w") as file:
                file.write("")
            self.load_notes()
    
    def delete_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            return
        note_path = os.path.join(NOTES_DIR, self.note_listbox.get(selection[0]))
        if messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{note_path}'?"):
            os.remove(note_path)
            self.load_notes()
            self.text_editor.delete(1.0, tk.END)
            self.current_note = None
    
    def rename_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            return
        old_note_path = os.path.join(NOTES_DIR, self.note_listbox.get(selection[0]))
        new_name = simpledialog.askstring("Rename Note", "Enter new name:")
        if new_name:
            new_note_path = os.path.join(NOTES_DIR, new_name + ".txt")
            os.rename(old_note_path, new_note_path)
            self.load_notes()
    
    def move_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            return
        note_path = os.path.join(NOTES_DIR, self.note_listbox.get(selection[0]))
        new_folder = filedialog.askdirectory(initialdir=NOTES_DIR, title="Select Folder")
        if new_folder:
            new_path = os.path.join(new_folder, os.path.basename(note_path))
            os.rename(note_path, new_path)
            self.load_notes()
    
    def new_folder(self):
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            folder_path = os.path.join(NOTES_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            self.load_notes()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteEditorApp(root)
    root.mainloop()