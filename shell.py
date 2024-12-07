import customtkinter as ctk
import lexer

# Appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# List of keywords
keywords = [
    "domain", "expansion", "null", "int", "float", "string", "bool", 
    "restrict", "invoke", "capture", "true", "false", 
    "vow", "else vow", "else", "boogie", "woogie", 
    "default", "cycle", "sustain", "perform", 
    "dismiss", "hop", "recall", "cleave", 
    "dismantle", "len()", "curse"
]

# Function to process the input (color highlighting only)
def process_input_color(event=None):
    text = input_text.get("1.0", "end").strip()  # Get input text
    if not text:
        return

    # Clear previous highlights
    input_text.tag_remove("purple", "1.0", "end")
    input_text.tag_remove("comment", "1.0", "end")
    input_text.tag_remove("string", "1.0", "end")  # Clear string highlights

    # Highlight keywords from the list
    for keyword in keywords:
        start_index = "1.0"
        while True:
            # Find the next occurrence of the keyword
            start_index = input_text.search(keyword, start_index, stopindex="end")
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            # Apply the tag to the keyword
            input_text.tag_add("purple", start_index, end_index)
            start_index = end_index  # Move to the next character after the keyword

    # Define the tag for magenta color (keyword highlight)
    input_text.tag_config("purple", foreground="#f396d3")

    # Highlight single-line comments starting with '#'
    start_index = "1.0"
    while True:
        start_index = input_text.search("#", start_index, stopindex="end")
        if not start_index:
            break
        line_end = input_text.index(f"{start_index} lineend")  # End of the line
        input_text.tag_add("comment", start_index, line_end)
        start_index = line_end

    # Highlight multi-line comments starting with '#$' and ending with '$#'
    start_index = "1.0"
    while True:
        start_index = input_text.search("#\\$", start_index, stopindex="end", regexp=True)
        if not start_index:
            break
        end_index = input_text.search("\\$#", start_index, stopindex="end", regexp=True)
        if not end_index:
            end_index = input_text.index("end")  # If no closing tag, highlight to the end
        else:
            end_index = f"{end_index}+2c"  # Include '$#' in the highlight
        input_text.tag_add("comment", start_index, end_index)
        start_index = end_index

    # Define the tag for green color (comment highlight)
    input_text.tag_config("comment", foreground="#999999")

    # Highlight strings, including multi-line strings
    start_index = "1.0"
    while True:
        # Find the starting double quote for strings
        start_index = input_text.search(r'"', start_index, stopindex="end", regexp=True)
        if not start_index:
            break

        # Check if there is a closing quote on the same line
        end_index = input_text.search(r'"', f"{start_index}+1c", stopindex="end", regexp=True)
        
        if not end_index:
            # If there's no closing quote on the same line, find it in subsequent lines
            # Search for a quote in the next lines
            end_index = input_text.search(r'"', f"{start_index}+1l", stopindex="end", regexp=True)
        
        if not end_index:
            end_index = input_text.index("end")  # If no closing quote, highlight until the end
        else:
            end_index = f"{end_index}+1c"  # Include the closing double quote in the highlight

        # Apply the tag to the string
        input_text.tag_add("string", start_index, end_index)
        start_index = end_index  # Move past the highlighted string

    # Define the tag for orange color (string highlight)
    input_text.tag_config("string", foreground="#FFCA4B")

def process_input(event=None):
    text = input_text.get("1.0", "end").strip()  # Get input text
    if not text:
        return

    # Run lexer
    tokens, error = lexer.run('<stdin>', text)

    # Update tokens output
    tokens_output.configure(state="normal")  # Enable editing temporarily
    tokens_output.delete("1.0", "end")  # Clear previous tokens
    if tokens:
        numbered_tokens = [f"{i + 1}:  {token}" for i, token in enumerate(tokens)]  # Add line numbers
        tokens_output.insert("1.0", '\n'.join(numbered_tokens)) 
    tokens_output.configure(state="disabled")  # Disable editing after update

    # Update error output
    error_output.configure(state="normal")  # Enable editing temporarily
    error_output.delete("1.0", "end")  # Clear previous errors
    # Update error output
    error_output.delete("1.0", "end")  # Clear previous errors
    if error:
        error_output.insert("1.0", error.as_string())
    error_output.configure(state="disabled") # disable editing after update

# Create the main app window
app = ctk.CTk()
app.title("DOM Compiler")
app.geometry("700x545")  # Adjust width to fit the tokens area comfortably
app.resizable(False, False)

# Change the window icon
try:
    app.iconbitmap("dom_logo.ico")  # Replace with your .ico file path
except Exception as e:
    print(f"Could not set icon: {e}")

# Input section
input_label = ctk.CTkLabel(app, text="Input Code:", font=("Arial", 16))
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Input Text widget without scrollbars and no wrapping
input_text = ctk.CTkTextbox(app, width=600, height=280, font=("Verdana", 14), wrap="none")
input_text.grid(row=1, column=0, padx=20, pady=0, sticky="n")

# Add support for text tagging (needed for highlighting)
input_text.configure(state="normal")  # Ensure text is editable

# Bind the key release event to trigger input processing (for color highlighting only)
input_text.bind("<KeyRelease>", process_input_color)

# Create Tokenize Input button to process tokens and errors
process_button = ctk.CTkButton(app, text="Tokenize Input", command=process_input, width=390)
process_button.grid(row=2, column=0, padx=10, pady=10, sticky="n")

# Tokens section (right-side rectangle)
tokens_label = ctk.CTkLabel(app, text="Tokens:", font=("Arial", 16))
tokens_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

tokens_output = ctk.CTkTextbox(app, width=230, height=485, font=("Verdana", 14), state="disabled", wrap="none")  # Set to disabled initially
tokens_output.grid(row=1, rowspan=5, column=1, padx=20, pady=0, sticky="n")

# Error section (below input text)
error_label = ctk.CTkLabel(app, text="Errors:", font=("Arial", 16))
error_label.grid(row=3, column=0, padx=5, pady=5, sticky="n")

# Error textbox without scrollbars and no wrapping
error_output = ctk.CTkTextbox(app, width=600, height=119, font=("Consolas", 14), state="disabled", wrap="none")  # Set to disabled initially
error_output.grid(row=4, column=0, padx=20, pady=0, sticky="s")

# Column and row configurations
app.grid_columnconfigure(0, weight=1)  # Input column
app.grid_columnconfigure(1, weight=0)  # Tokens column
app.grid_rowconfigure(1, weight=0)  # Ensure proper expansion

# Start the application
app.mainloop()
