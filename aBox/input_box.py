from blessed import Terminal

term = Terminal()


def create_box() -> None:
    """Creates a text-input-box"""
    print(term.home + term.clear)
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():

        # Makes it so you can type and make new lines in the terminal.
        key = ""
        display_string = ""
        lines = 2
        while key != "\x1b":
            key = term.inkey()
            if key and not key.is_sequence:
                display_string += key

            elif key.is_sequence:
                if key.name == "KEY_BACKSPACE":
                    if display_string.endswith("\n "):
                        lines -= 1
                        display_string = display_string[:-1]
                    display_string = display_string[:-1]

                elif key.name == "KEY_ENTER":
                    lines += 1
                    display_string += "\n "

            for y in range(1, lines+1):
                print(term.move_xy(0, y) + " "*(term.width-2))

            print(term.move_xy(1, 1) + display_string + term.blink("⎸"))


if __name__ == "__main__":
    create_box()
