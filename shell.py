import lexer

while True:
    text = input('DOM > ')
    result, error = lexer.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)