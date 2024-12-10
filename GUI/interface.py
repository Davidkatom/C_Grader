import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

from c_file_runner import run_file

input = "C:/Grading/Now/ass2/Input.txt"
output_file = "C:/Grading/Now/ass2/Output.txt"
c_file = ""
checkbox_states = {}

def load_text_from_file(filepath):
    global c_file
    c_file = filepath
    filepath = filepath.strip('{}')
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        text_area.edit_separator()  # Start undo block
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)
        text_area.edit_separator()  # End undo block
        title_label.config(text=filepath.split('/')[-1])  # Update title with file name
    except Exception as e:
        print(f"Error loading file: {e}")

def drop_file(event):
    dropped_files = event.data
    if dropped_files:
        first_file = dropped_files.split(' ')[0]
        load_text_from_file(first_file)

def compile_and_run():
    global input, output_file
    input = input_file_entry.get()
    output_file = output_file_entry.get()
    print(f"Compiling and running with input: {input}, output: {output_file}")
    output = run_file(c_file, input)
    right_text_area.config(state='normal')
    right_text_area.delete("1.0", "end")
    right_text_area.insert("1.0", output)
    right_text_area.config(state='disabled')

def toggle_checkbox(option):
    checkbox_states[option] = not checkbox_states.get(option, False)
    print(f"{option} set to {checkbox_states[option]}")

# Create a DnD-enabled root window
root = TkinterDnD.Tk()
root.title("Text Editor with Compile and Run, Split Views, and Options")

# Configure main window grid
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=1)

# Title Label for file name
title_label = tk.Label(root, text="", font=("Helvetica", 14), anchor="center")
title_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)

# Top Frame for buttons and input/output fields
top_frame = tk.Frame(root)
top_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
top_frame.columnconfigure((0, 1, 2, 3), weight=1)

# Compile and Run Button
compile_button = tk.Button(top_frame, text="Compile and Run", command=compile_and_run)
compile_button.grid(row=0, column=0, padx=5, pady=5)

# Input and Output File Fields
input_file_label = tk.Label(top_frame, text="Input File:")
input_file_label.grid(row=1, column=0, sticky="e", padx=5)
input_file_entry = tk.Entry(top_frame, width=40)
input_file_entry.insert(0, input)
input_file_entry.grid(row=1, column=1, padx=5)

output_file_label = tk.Label(top_frame, text="Output File:")
output_file_label.grid(row=1, column=2, sticky="e", padx=5)
output_file_entry = tk.Entry(top_frame, width=40)
output_file_entry.insert(0, output_file)
output_file_entry.grid(row=1, column=3, padx=5)

# Left Frame with vertical buttons
left_frame = tk.Frame(root)
left_frame.grid(row=2, column=0, sticky="nsw")

# Add checkboxes
checkbox_label = tk.Label(left_frame, text="Options:")
checkbox_label.grid(row=0, column=0, sticky="w")
checkbox_options = ["Line breakers", "Remove return 0", "No comments", "Not compiling"]
for i, option in enumerate(checkbox_options, start=1):
    state_var = tk.BooleanVar(value=False)
    checkbox_states[option] = state_var.get()
    checkbox = tk.Checkbutton(
        left_frame, text=option, variable=state_var, command=lambda opt=option: toggle_checkbox(opt)
    )
    checkbox.grid(row=i, column=0, sticky="w")

# Center Frame for scrollable text (editable)
center_frame = tk.Frame(root)
center_frame.grid(row=2, column=1, sticky="nsew")
center_frame.rowconfigure(0, weight=1)
center_frame.columnconfigure(0, weight=1)

text_area = tk.Text(center_frame, wrap="word", undo=True, autoseparator=False)
text_area.grid(row=0, column=0, sticky="nsew")

center_scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=text_area.yview)
center_scrollbar.grid(row=0, column=1, sticky="ns")
text_area.config(yscrollcommand=center_scrollbar.set)

# Right Frame for split scrollable text areas (non-editable)
right_frame = tk.Frame(root)
right_frame.grid(row=2, column=2, sticky="nsew")
right_frame.rowconfigure((0, 1), weight=1)
right_frame.columnconfigure(0, weight=1)

right_text_area = tk.Text(right_frame, wrap="word", state="normal", height=15)
right_text_area.grid(row=0, column=0, sticky="nsew")
right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_text_area.yview)
right_scrollbar.grid(row=0, column=1, sticky="ns")
right_text_area.config(yscrollcommand=right_scrollbar.set)

bottom_text_area = tk.Text(right_frame, wrap="word", state="normal", height=10)
bottom_text_area.grid(row=1, column=0, sticky="nsew")
bottom_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=bottom_text_area.yview)
bottom_scrollbar.grid(row=1, column=1, sticky="ns")
bottom_text_area.config(yscrollcommand=bottom_scrollbar.set)

# Initialize right text areas
right_text_area.insert("1.0", "Right Text Area - Top")
right_text_area.config(state="disabled")
bottom_text_area.insert("1.0", "Right Text Area - Bottom")
bottom_text_area.config(state="disabled")

# Enable Drag-and-Drop
text_area.drop_target_register(DND_FILES)
text_area.dnd_bind('<<Drop>>', drop_file)

# Add drag-and-drop to the input and output file entry fields
input_file_entry.drop_target_register(DND_FILES)
input_file_entry.dnd_bind('<<Drop>>', lambda e: input_file_entry.delete(0, tk.END) or input_file_entry.insert(0, e.data.strip('{}')))

output_file_entry.drop_target_register(DND_FILES)
output_file_entry.dnd_bind('<<Drop>>', lambda e: output_file_entry.delete(0, tk.END) or output_file_entry.insert(0, e.data.strip('{}')))

root.mainloop()
