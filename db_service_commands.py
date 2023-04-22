def null_fix(*arguments):
    #html gives everything to the send form as string, None gives empty string. Here the function converts all valid id's to integers. 
    fixed_arguments = []
    for argument in arguments:
        if argument == '':
            fixed_arguments.append(None)
        else:
            fixed_arguments.append(int(argument))
    return fixed_arguments