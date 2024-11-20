import customtkinter as ctk
import lexer

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  

# Function to process the input using the lexer and display results
def process_input():
    text = input_text.get("1.0", "end").strip()  # Get input text
    if not text:
        return
    
    # Run lexer
    tokens, error = lexer.run('<stdin>', text)

    # Update tokens output
    tokens_output.delete("1.0", "end")  # Clear previous tokens
    if tokens:
        tokens_output.insert("1.0", '\n'.join(map(str, tokens)))

    # Update error output
    error_output.delete("1.0", "end")  # Clear previous errors
    if error:
        error_output.insert("1.0", error.as_string())
    
app = ctk.CTk()
app.title("DOM Compiler GUI")
app.geometry("800x850")
app.resizable(False, False)

input_label = ctk.CTkLabel(app, text="Input Code:", font=("Arial", 16))
input_label.pack(pady=(20, 5))

input_text = ctk.CTkTextbox(app, width=750, height=350, font=("Courier", 20))
input_text.pack(pady=10)

process_button = ctk.CTkButton(app, text="Tokenize Input", command=process_input)
process_button.pack(pady=10)

tokens_label = ctk.CTkLabel(app, text="Tokens:", font=("Arial", 16))
tokens_label.pack(pady=(20, 5))

tokens_output = ctk.CTkTextbox(app, width=750, height=100, font=("Courier", 20), state="normal")
tokens_output.pack(pady=10)

error_label = ctk.CTkLabel(app, text="Errors:", font=("Arial", 16))
error_label.pack(pady=(20, 5))

error_output = ctk.CTkTextbox(app, width=750, height=100, font=("Courier", 20), state="normal")
error_output.pack(pady=10)

app.mainloop()
