from blessed import Terminal

term = Terminal()


def create_box() -> None:
    """Creates a text-input-box"""
    print(term.home + term.clear)
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():

        # Makes it so you can type and make new lines in the terminal.
        key = ""
        display_list = [""]
        cx = 0
        cy = 0

        hl_word_colors = [
            {"word":"(","color":term.orange},
            {"word":")","color":term.orange},
            {"word":"move","color":term.yellow},
            {"word":"grab","color":term.yellow},
            {"word":"func","color":term.steelblue4},
            {"word":"print","color":term.yellow},
            {"word":"up","color":term.hblue},
            {"word":"down","color":term.hblue},
            {"word":"left","color":term.hblue},
            {"word":"right","color":term.hblue},
            {"word":"begin","color":term.purple},
            {"word":"loop","color":term.red},
            {"word":"set","color":term.green},
        ]

        hl_num_color = term.color_rgb(255, 0, 0)

        while key != "\x1b":
            key = term.inkey()
            if key and not key.is_sequence:
                display_list[cy] = display_list[cy][:cx] + key + display_list[cy][cx:]
                cx += 1

            elif key.is_sequence:
                if key.name == "KEY_ENTER":
                    display_list.insert(cy + 1, display_list[cy][cx:])
                    display_list[cy] = display_list[cy][:cx]
                    cy += 1
                    cx = 0

                elif key.name == "KEY_BACKSPACE":
                    if cx <= 0:
                        if cy > 0:
                            cx = len(display_list[cy - 1])
                            if len(display_list[cy]) > 0:
                                display_list[cy - 1] += display_list[cy]
                            display_list.pop(cy)
                            cy -= 1
                    else:
                        display_list[cy] = display_list[cy][:cx - 1] + display_list[cy][cx:]
                        cx -=1

                elif key.name == "KEY_DELETE":
                    if cx < len(display_list[cy]):
                        display_list[cy] = display_list[cy][:cx] + display_list[cy][cx +1 :]
                    elif cy < len(display_list) - 1:
                        display_list[cy] += display_list[cy + 1]
                        display_list.pop(cy + 1)
                        
                elif key.name == "KEY_LEFT":
                    if cx <= 0:
                        if cy > 0:
                            cy -= 1
                            cx = len(display_list[cy])
                    else:
                        cx -= 1

                elif key.name == "KEY_RIGHT":
                    if cx >= len(display_list[cy]):
                        if cy < len(display_list) - 1:
                            cy += 1
                            cx = 0
                    else:
                        cx += 1

                elif key.name == "KEY_UP":
                    if cy > 0:
                        cy -= 1
                        cx = min(cx, len(display_list[cy]))

                elif key.name == "KEY_DOWN":
                    if cy < len(display_list) - 1:
                        cy += 1
                        cx = min(cx, len(display_list[cy]))

                elif key.name == "KEY_HOME":
                    cx = 0

                elif key.name == "KEY_END":
                    cx = len(display_list[cy])


            for y in range(1, len(display_list)+3):
                print(term.move_xy(0, y) + " "*(term.width-2))
            #print(term.move_xy(0, len(display_list)) + " "*(term.width-2))#not working jet


            for y, current_list in enumerate(display_list):
                #print(term.move_xy(1, y + 1) + current_list)
                #for i in range(1, 10):
                #    current_list = current_list.replace(str(i), term.color_rgb(255, 0, 0) + str(i) + term.normal) #this is very broken for some reason
                for i in hl_word_colors:
                    current_list = current_list.replace(i['word'], i['color']+ i['word'] + term.normal)
                print(term.move_xy(1, y + 1) + current_list)

                #for x, current_char in enumerate(current_list):
                #    print(term.move_xy(x + 1, y + 1) + current_char)

            
            #cursor
            print(term.move_xy(cx + 1, cy + 1) + term.on_white + display_list[cy][cx:cx+1])
            if not display_list[cy][cx:cx+1]:
                print(term.move_xy(cx + 1, cy + 1) + "⎸")
            print(term.normal)

            #print(term.move_xy(0, cy + 10),"Dobug:", cx, cy, key, key.name) #for debuging


if __name__ == "__main__":
    create_box()
