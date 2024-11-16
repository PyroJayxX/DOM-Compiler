import dom

while True:
    text = input('DOM > ')
    result, error = dom.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)