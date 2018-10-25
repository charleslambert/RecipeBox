from fractions import Fraction


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys
    import tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()


def y_n_prompt(prompt, default):
    if default == "y":
        y_n = "[Y/n]"
    else:
        y_n = "[y/N]"

    print(prompt, y_n)
    while True:
        char = getch()

        if char == "\r":
            return default
        if char in ["y", "Y", "n", "N"]:
            return char.lower()


def list_items(prompt, items):

    print(prompt)
    for i, item in enumerate(items):
        print(f"  {i}: {item}")

    while True:
        try:
            selection = int(getch())
            if selection in range(len(items)):
                return selection
        except ValueError:
            pass


def sanitized_input(prompt, typeof):
    while True:
        try:
            inp = typeof(input(prompt))
            return inp
        except ValueError:
            print(f"Should be {typeof}")


def amount_prompt(prompt):
    while True:
        try:
            inp = input(prompt).split(" ")
            if len(inp) < 2:
                return Fraction(inp[0])

            return Fraction(inp[0]) + Fraction(inp[1])
        except (ValueError, NameError):
            print(f"Invalid amout can be whole, fraction or mixed number")
