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
    tokens_output.configure(state="normal")  # Enable editing temporarily
    tokens_output.delete("1.0", "end")  # Clear previous tokens
    if tokens:
        numbered_tokens = [f"{i + 1}:  {token}" for i, token in enumerate(tokens)]  # Add line numbers
        tokens_output.insert("1.0", '\n'.join(numbered_tokens))
    tokens_output.configure(state="disabled")  # Disable editing after update

    # Update error output
    error_output.configure(state="normal")  # Enable editing temporarily
    error_output.delete("1.0", "end")  # Clear previous errors
    if errors:
        error_output.insert("1.0", '\n'.join(error.as_string() for error in errors))
    error_output.configure(state="disabled")  # Disable editing after update

# Create the main app window
app = ctk.CTk()
app.title("DOM Compiler GUI")
app.geometry("700x545")  # Adjust width to fit the tokens area comfortably
app.resizable(False, False)

# Input section
input_label = ctk.CTkLabel(app, text="Input Code:", font=("Arial", 16))
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Input Text widget without scrollbars and no wrapping
input_text = ctk.CTkTextbox(app, width=600, height=280, font=("Courier", 14), wrap="none")
input_text.grid(row=1, column=0, padx=20, pady=0, sticky="n")

process_button = ctk.CTkButton(app, text="Tokenize Input", command=process_input, width=390)
process_button.grid(row=2, column=0, padx=10, pady=10, sticky="n")

# Tokens section (right-side rectangle)
tokens_label = ctk.CTkLabel(app, text="Tokens:", font=("Arial", 16))
tokens_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

tokens_output = ctk.CTkTextbox(app, width=230, height=485, font=("Courier", 14), state="disabled", wrap="none")  # Set to disabled initially
tokens_output.grid(row=1, rowspan=5, column=1, padx=20, pady=0, sticky="n")

# Error section (below input text)
error_label = ctk.CTkLabel(app, text="Errors:", font=("Arial", 16))
error_label.grid(row=3, column=0, padx=5, pady=5, sticky="n")

# Error textbox without scrollbars and no wrapping
error_output = ctk.CTkTextbox(app, width=600, height=119, font=("Courier", 14), state="disabled", wrap="none")  # Set to disabled initially
error_output.grid(row=4, column=0, padx=20, pady=0, sticky="s")

# Column and row configurations
app.grid_columnconfigure(0, weight=1)  # Input column
app.grid_columnconfigure(1, weight=0)  # Tokens column
app.grid_rowconfigure(1, weight=0)  # Ensure proper expansion

# Start the application
app.mainloop()
