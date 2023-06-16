# Ansi escape codes for games with a Terminal Interface
# Will only work with os.system("") !
COLORCODE = {
        "Blue": "\033[94m",
        "Green": "\033[92m",
        "Red": "\033[91m",
        "Yellow": "\033[93m",
        "Black": "\033[5m",
        "MAGENTA": "\033[95m",
        "ENDC": "\033[0m",
    }
STYLE = {
        "BOLD": "\033[1m",
        "ENDS": "\033[0m"
}

def select_option(min, max):
    """
    General selection function that checks for Value_error, Type_error.
    Ensures value is between min and max (inclusive).
    """
    while True:
            try:
                selection = int(input('\nSelect an option: '))
            except (TypeError, ValueError):
                print('Invalid selection.')
                continue
            if selection < min or selection > max:
                print('Selection out of range.')
                continue
            else:
                break

    return selection