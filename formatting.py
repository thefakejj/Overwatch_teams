from string import whitespace, ascii_letters, digits, punctuation
import db_select

def format_fully(input):
    input = input.strip()
    return input
    # if there were to be more formatting

def username_invalid_characters(username):
    invalid_punctuation = punctuation.replace("_", '')
    invalid_punctuation = invalid_punctuation.replace(".", '')
    if whitespace in username:
        return True
    elif invalid_punctuation in username:
        return True
    return False

def people_name_description(name):
    # returns "okay" if no errors in format, otherwise returns error message
    if len(name) < 2:
        message = "Name is too short! A person's name should be at least 2 characters long."
    elif len(name) > 20:
        message = "Name is too long! A person's should be at most 20 characters long."
    elif whitespace in name or punctuation in name:
        message = "Name contains invalid characters! Please input a name that includes just letters or numbers."
    else:
        message = "okay"
    return message

def tournaments_name_description(name):
    # returns "okay" if no errors in format, otherwise returns error message
    if len(name) < 3:
        message = "Name is too short! A tournament's name should be at least 3 characters long."
    elif len(name) > 100:
        message = "Name is too long! A tournament's name should be at most 100 characters long."
    elif db_select.has_tournament_been_added(name):
        message = "Tournament of this name already exists"
    else:
        message = "okay"
    return message

def teams_name_description(name):
    # returns "okay" if no errors in format, otherwise returns error message
    if len(name) < 3:
        message = "Name is too short! A team's name should be at least 3 characters long."
    elif len(name) > 80:
        message = "Name is too long! A team's name should be at most 80 characters long."
    elif db_select.has_team_been_added(name):
        message = "Team of this name already exists!"
    else:
        message = "okay"
    return message