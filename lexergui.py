import tkinter as tk
from tkinter import ttk
import lexer

app = tk.Tk()
app.title("DOM Lexer")
app.geometry("1000x630")
app.resizable(False, False)
app.option_add("*tearOff", False)  # This is always a good idea

style = ttk.Style()
try:
    app.tk.call("source", "./Dependencies/forest-dark.tcl")  # Ensure forest-dark.tcl is in the same directory
    style.theme_use("forest-dark")
except Exception as e:
    print(f"Error loading Forest theme: {e}")

try:
    app.iconbitmap("./Dependencies/dom_logo.ico")
except Exception as e:
    print(f"Could not set icon: {e}")

keywords = [
    "domain", "expansion", "null", "int", "float", "string", "bool",
    "restrict", "invoke", "capture", "true", "false",
    "vow", "else", "boogie", "woogie",
    "default", "cycle", "sustain", "perform",
    "dismiss", "hop", "recall", "cleave",
    "dismantle", "len", "curse"
]

def apply_syntax_highlighting(event=None):
    text = input_text.get("1.0", "end").strip()
    if not text:
        return

    input_text.tag_remove("keyword", "1.0", "end")
    input_text.tag_remove("comment", "1.0", "end")
    input_text.tag_remove("string", "1.0", "end")

    for keyword in keywords:
        start_index = "1.0"
        while True:
            start_index = input_text.search(keyword, start_index, stopindex="end")
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            input_text.tag_add("keyword", start_index, end_index)
            start_index = end_index

    input_text.tag_config("keyword", foreground="#f396d3")

    start_index = "1.0"
    while True:
        start_index = input_text.search("#", start_index, stopindex="end")
        if not start_index:
            break
        line_end = input_text.index(f"{start_index} lineend")
        input_text.tag_add("comment", start_index, line_end)
        start_index = line_end

    input_text.tag_config("comment", foreground="#999999")

    start_index = "1.0"
    while True:
        start_index = input_text.search(r'"', start_index, stopindex="end", regexp=True)
        if not start_index:
            break
        end_index = input_text.search(r'"', f"{start_index}+1c", stopindex="end", regexp=True)
        if not end_index:
            end_index = input_text.index("end")
        else:
            end_index = f"{end_index}+1c"
        input_text.tag_add("string", start_index, end_index)
        start_index = end_index

    input_text.tag_config("string", foreground="#FFCA4B")

def process_input():
    text = input_text.get("1.0", "end").strip()
    if not text:
        return

    tokens, error = lexer.run('<stdin>', text)

    for row in table.get_children():
        table.delete(row)

    if tokens:
        for token in tokens:
            table.insert("", "end", values=(token.value, token.type, token.value))

    error_output.config(state="normal")
    error_output.delete("1.0", "end")
    if error:
        error_output.insert("1.0", error.as_string())
    error_output.config(state="disabled")

# Input Section
input_label = ttk.Label(app, text="Input Code:", font=("TkDefaultFont", 11))
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

input_text = tk.Text(app, width=85, height=20, font=("Verdana", 10), wrap="none")
input_text.grid(row=1, column=0, padx=20, pady=0, sticky="n")
input_text.bind("<KeyRelease>", apply_syntax_highlighting)

process_button = ttk.Button(app, text="Tokenize Input", command=process_input, style="Accent.TButton")
process_button.grid(row=2, column=0, padx=20, pady=12, sticky="n")

# Error Output Section
error_label = ttk.Label(app, text="Error:", font=("TkDefaultFont", 11))
error_label.grid(row=3, column=0, padx=20, pady=5, sticky="n")

error_output = tk.Text(app, width=85, height=7, font=("Consolas", 10), state="disabled", wrap="none")
error_output.grid(row=4, column=0, padx=20, pady=0, sticky="s")

# Table Section
table_frame = ttk.Frame(app)
table_frame.grid(row=1, rowspan=5, column=1, padx=20, pady=0, sticky="n")

columns = ("Lexeme", "Token Type", "Attribute")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
for col in columns:
    table.heading(col, text=col, anchor="center")
    table.column(col, anchor="center", width=120)

v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
v_scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=v_scrollbar.set)
table.pack(fill="both", expand=True)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=0)
app.grid_rowconfigure(1, weight=0)

app.mainloop()
