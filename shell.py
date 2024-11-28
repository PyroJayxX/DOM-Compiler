import customtkinter as ctk
import lexer

# Appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Function to process the input using the lexer and display results
def process_input():
    text = input_text.get("1.0", "end").strip()  # Get input text
    if not text:
        return
    
    # Run lexer
    tokens, errors = lexer.run('<stdin>', text)

    # Update tokens output
    tokens_output.delete("1.0", "end")  # Clear previous tokens
    if tokens:
        numbered_tokens = [f"{i + 1}:  {token}" for i, token in enumerate(tokens)]  # Add line numbers
        tokens_output.insert("1.0", '\n'.join(numbered_tokens))

    # Update error output
    error_output.delete("1.0", "end")  # Clear previous errors
    if errors:
        error_output.insert("1.0", '\n'.join(error.as_string() for error in errors))
    
    # Adjust scrollbar visibility
    adjust_scrollbar_visibility()

def adjust_scrollbar_visibility():
    error_output.update_idletasks()
    text_width = error_output.bbox("end")[0] if error_output.bbox("end") else 0
    widget_width = error_output.winfo_width()
    
    # Show or hide the scrollbar based on content width
    if text_width > widget_width:
        error_scrollbar.grid()  # Show scrollbar
    else:
        error_scrollbar.grid_remove()  # Hide scrollbar

# Create the main app window
app = ctk.CTk()
app.title("DOM Compiler GUI")
app.geometry("700x545")  # Adjust width to fit the tokens area comfortably
app.resizable(False, False)

# Input section
input_label = ctk.CTkLabel(app, text="Input Code:", font=("Arial", 16))
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

input_text = ctk.CTkTextbox(app, width=600, height=280, font=("Courier", 14))
input_text.grid(row=1, column=0, padx=20, pady=0, sticky="n")

process_button = ctk.CTkButton(app, text="Tokenize Input", command=process_input, width=390)
process_button.grid(row=2, column=0, padx=10, pady=10, sticky="n")

# Tokens section (right-side rectangle)
tokens_label = ctk.CTkLabel(app, text="Tokens:", font=("Arial", 16))
tokens_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

tokens_output = ctk.CTkTextbox(app, width=230, height=485, font=("Courier", 14), state="normal")
tokens_output.grid(row=1, rowspan=5, column=1, padx=20, pady=0, sticky="n")

# Error section (below input text)
error_label = ctk.CTkLabel(app, text="Errors:", font=("Arial", 16))
error_label.grid(row=3, column=0, padx=5, pady=5, sticky="n")

# Error textbox with horizontal scrollbar
error_output = ctk.CTkTextbox(app, width=600, height=119, font=("Courier", 14), state="normal", wrap="none")
error_output.grid(row=4, column=0, padx=20, pady=0, sticky="s")

# Add horizontal scrollbar for errors
error_scrollbar = ctk.CTkScrollbar(app, orientation="horizontal", command=error_output.xview)
error_scrollbar.grid(row=5, column=0, sticky="ew", padx=20)
error_output.configure(xscrollcommand=error_scrollbar.set)

# Initially hide the scrollbar
adjust_scrollbar_visibility()

# Column and row configurations
app.grid_columnconfigure(0, weight=1)  # Input column
app.grid_columnconfigure(1, weight=0)  # Tokens column
app.grid_rowconfigure(1, weight=0)  # Ensure proper expansion

# Start the application
app.mainloop()
