import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

# Define paths
FOLDER_TO_CLEAR = "D:\\hackathon\\Maze\\input"
FOLDER_TO_COPY_IMAGES = "D:\\hackathon\\Maze\\input"
PDF_PATH = "D:\\hackathon\\Maze\\outputs\\output.pdf"

# Supported image formats
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

def run_python_file():
    """Runs start.py and opens the output PDF if it exists."""
    try:
        os.system('python start.py')
        status_var.set("✅ Mazes solved successfully.")

        if os.path.exists(PDF_PATH):
            os.startfile(PDF_PATH)  # Open PDF on Windows
        else:
            messagebox.showerror("Error", f"Output PDF not found at:\n{PDF_PATH}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute start.py:\n{e}")

def clear_folder():
    """Clears all files in the input folder."""
    if not os.path.exists(FOLDER_TO_CLEAR):
        messagebox.showerror("Error", f"The folder {FOLDER_TO_CLEAR} does not exist.")
        return

    try:
        for item in os.listdir(FOLDER_TO_CLEAR):
            item_path = os.path.join(FOLDER_TO_CLEAR, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        status_var.set("🗑 Folder cleared successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear folder:\n{e}")

def handle_drop(event):
    """Handles the drag & drop event for image files."""
    dropped_files = event.data.strip()
    file_paths = root.tk.splitlist(dropped_files)

    for file_path in file_paths:
        file_path = file_path.strip()

        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file_path)[-1].lower()
            if file_ext in SUPPORTED_IMAGE_FORMATS:
                try:
                    shutil.copy(file_path, FOLDER_TO_COPY_IMAGES)
                    status_var.set(f"📁 File copied: {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy file:\n{e}")
            else:
                messagebox.showwarning("Warning", f"Unsupported file type: {file_ext}")
        else:
            messagebox.showwarning("Warning", f"Invalid file path: {file_path}")

# Initialize TkinterDnD
root = TkinterDnD.Tk()
root.title("Cool File Manager")
root.geometry("520x350")
root.configure(bg="#1E1E1E")

# Title Label
title_label = tk.Label(root, text="📂 File Manager", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E")
title_label.pack(pady=10)

# Button styles
button_style = {"font": ("Arial", 12), "width": 20, "borderwidth": 0, "relief": "flat"}

def on_enter(e, widget, color):
    widget.config(bg=color)

def on_leave(e, widget, color):
    widget.config(bg=color)

# Run button
run_button = tk.Button(root, text="▶ Solve the Maze", **button_style, bg="#007BFF", fg="white", command=run_python_file)
run_button.pack(pady=5)
run_button.bind("<Enter>", lambda e: on_enter(e, run_button, "#0056b3"))
run_button.bind("<Leave>", lambda e: on_leave(e, run_button, "#007BFF"))

# Clear button
clear_button = tk.Button(root, text="🗑 Clear Input", **button_style, bg="#DC3545", fg="white", command=clear_folder)
clear_button.pack(pady=5)
clear_button.bind("<Enter>", lambda e: on_enter(e, clear_button, "#A71D2A"))
clear_button.bind("<Leave>", lambda e: on_leave(e, clear_button, "#DC3545"))

# Drag & Drop Label
drop_label = tk.Label(
    root, text="📂 Drag & Drop an Image Here", font=("Arial", 12), bg="#444", fg="white", padx=10, pady=5, relief="ridge"
)
drop_label.pack(pady=15, fill="x", padx=20)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", handle_drop)

# Status bar
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 10), fg="lightgray", bg="#1E1E1E")
status_label.pack(pady=10)

root.mainloop()
