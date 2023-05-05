from string import whitespace, ascii_letters, digits, punctuation

def strip(string):
    return string.strip()

def format_fully(input):
    input = strip(input)
    return input
    # if there were to be more formatting

def username_invalid_characters(string):
    invalid_punctuation = punctuation.replace("_", '')
    invalid_punctuation = invalid_punctuation.replace(".", '')
    if whitespace in string:
        return True
    elif invalid_punctuation in string:
        return True
    return False
    