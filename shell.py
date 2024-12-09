import customtkinter as ctk
import lexer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

keywords = [
    "domain", "expansion", "null", "int", "float", "string", "bool", 
    "restrict", "invoke", "capture", "true", "false", 
    "vow", "else vow", "else", "boogie", "woogie", 
    "default", "cycle", "sustain", "perform", 
    "dismiss", "hop", "recall", "cleave", 
    "dismantle", "len", "curse"
]

def process_input_color(event=None):                # function to process the input color
    text = input_text.get("1.0", "end").strip()     # Get input text
    if not text:
        return

    # clear previous highlights
    input_text.tag_remove("purple", "1.0", "end")
    input_text.tag_remove("comment", "1.0", "end")
    input_text.tag_remove("string", "1.0", "end")  # clear string highlights

    # highlight keywords from the list
    for keyword in keywords:
        start_index = "1.0"
        while True:
            # find the next occurrence of the keyword
            start_index = input_text.search(keyword, start_index, stopindex="end")
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            # apply the tag to the keyword
            input_text.tag_add("keyword", start_index, end_index)
            start_index = end_index  # Move to the next character after the keyword

    # define the tag for magenta color (keyword highlight)
    input_text.tag_config("keyword", foreground="#f396d3")

    # highlight single-line comments starting with '#'
    start_index = "1.0"
    while True:
        start_index = input_text.search("#", start_index, stopindex="end")
        if not start_index:
            break
        line_end = input_text.index(f"{start_index} lineend")  # End of the line
        input_text.tag_add("comment", start_index, line_end)
        start_index = line_end

    # highlight multi-line comments starting with '#$' and ending with '$#'
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

    # hefine the tag for gray color (comment highlight)
    input_text.tag_config("comment", foreground="#999999")

    # highlight strings, including multi-line strings
    start_index = "1.0"
    while True:
        # find the starting double quote for strings
        start_index = input_text.search(r'"', start_index, stopindex="end", regexp=True)
        if not start_index:
            break

        # check if there is a closing quote on the same line
        end_index = input_text.search(r'"', f"{start_index}+1c", stopindex="end", regexp=True)
        
        if not end_index:
            # if there's no closing quote on the same line, find it in subsequent lines
            # search for a quote in the next lines
            end_index = input_text.search(r'"', f"{start_index}+1l", stopindex="end", regexp=True)
        
        if not end_index:
            end_index = input_text.index("end")  # if no closing quote, highlight until the end
        else:
            end_index = f"{end_index}+1c"  # include the closing double quote in the highlight

        # apply the tag
        input_text.tag_add("string", start_index, end_index)
        start_index = end_index  # move past the highlighted string

    # tag color configuration
    input_text.tag_config("string", foreground="#FFCA4B")

def process_input(event=None):
    text = input_text.get("1.0", "end").strip()  # Get input text
    if not text:
        return

    # retrieve tokens, error from lexer 
    tokens, error = lexer.run('<stdin>', text)

    # update tokens output (token types)
    tokens_output.configure(state="normal")  # enable editing temporarily
    tokens_output.delete("1.0", "end")  # clear previous tokens
    if tokens:
        token_types = [f"{i + 1}:  {token.type}" for i, token in enumerate(tokens)]  # Add line numbers
        tokens_output.insert("1.0", '\n'.join(token_types))
    tokens_output.configure(state="disabled")  # disable editing after update

    # update lexeme output
    lexeme_output.configure(state="normal")  # enable editing temporarily
    lexeme_output.delete("1.0", "end")  # clear previous lexemes
    if tokens:
        lexemes = [f"{i + 1}:  {token.value}" for i, token in enumerate(tokens)]  # Add line numbers
        lexeme_output.insert("1.0", '\n'.join(lexemes))
    lexeme_output.configure(state="disabled")  # disable editing after update

    # update error output
    error_output.configure(state="normal")  # enable editing temporarily    
    error_output.delete("1.0", "end")  # clear previous errors
    if error:
        if isinstance(error, list):  # check if it's a list of errors
            error_messages = "\n".join(f"{idx + 1}. {e.as_string()}" for idx, e in enumerate(error))  # Add numbering
            error_output.insert("1.0", error_messages)
        else:
            error_output.insert("1.0", error.as_string())  # single error case
    error_output.configure(state="disabled")  # disable editing after update


app = ctk.CTk()
app.title("DOM Lexer")
app.geometry("1040x680")  # window resolution
app.resizable(False, False)

try:
    app.iconbitmap("dom_logo.ico") 
except Exception as e:
    print(f"Could not set icon: {e}")

# input section
input_label = ctk.CTkLabel(app, text="Input Code:", font=("Arial", 16))
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

input_text = ctk.CTkTextbox(app, width=700, height=400, font=("Verdana", 14), wrap="none")
input_text.grid(row=1, column=0, padx=20, pady=0, sticky="n")

input_text.configure(state="normal") 
input_text.bind("<KeyRelease>", process_input_color)

# tokenize Button
process_button = ctk.CTkButton(app, text="Tokenize Input", command=process_input, width=590)
process_button.grid(row=2, column=0, padx=20, pady=10, sticky="n")

# error section
error_label = ctk.CTkLabel(app, text="Errors:", font=("Arial", 16))
error_label.grid(row=3, column=0, padx=20, pady=5, sticky="n")

# error textbox
error_output = ctk.CTkTextbox(app, width=700, height=130, font=("Consolas", 14), state="disabled", wrap="none")
error_output.grid(row=4, column=0, padx=20, pady=0, sticky="s")

# tokens section 
tokens_label = ctk.CTkLabel(app, text="Token Type:", font=("Arial", 16))
tokens_label.grid(row=0, column=1, padx=0, pady=5, sticky="ew")

tokens_output = ctk.CTkTextbox(app, width=170, height=620, font=("Verdana", 14), state="disabled", wrap="none")
tokens_output.grid(row=1, rowspan=5, column=1, padx=20, pady=0, sticky="n")

# tokens section 
lexeme_label = ctk.CTkLabel(app, text="Lexemes:", font=("Arial", 16))
lexeme_label.grid(row=0, column=2, padx=20, pady=5, sticky="ew")

lexeme_output = ctk.CTkTextbox(app, width=170, height=620, font=("Verdana", 14), state="disabled", wrap="none")  
lexeme_output.grid(row=1, rowspan=5, column=2, padx=20, pady=0, sticky="n")

app.grid_columnconfigure(0, weight=1)  # input column
app.grid_columnconfigure(1, weight=0)  # tokens column
app.grid_columnconfigure(2, weight=0)  # lexeme column
app.grid_rowconfigure(1, weight=0) 

app.mainloop()
