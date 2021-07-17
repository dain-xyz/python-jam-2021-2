import asyncio
from run_levels import level_select

from blessed import Terminal

term = Terminal()
width = 0
height = 0

optimal_height = 35
optimal_width = 80

KEY_UP = 259
KEY_DOWN = 258
KEY_LEFT = 260
KEY_RIGHT = 261
KEY_ENTER = 343


def test_callback() -> None:
    """Tester callback function"""
    print("HELLO FROM A CALLBACK")


def quit(*args, **kwargs) -> None:
    """Callback to quit the program"""
    loop.stop()


options = [
    {"text": "New Game", 'x': 0, 'y': 0, 'callback': level_select, 'selected': True},
    # {"text": "Load Game", 'x': 0, 'y': 0, 'callback': None, 'selected': False},
    {"text": "Exit", 'x': 0, 'y': 0, 'callback': quit, 'selected': False}
]


def set_text(term: object, line: int, column: int, text: str) -> None:
    """Overwrite text on a given location"""
    print(term.home + term.move(line, column) + text)


async def draw_menu(term: object, width: int = term.width, height: int = term.height, redraw: bool = False) -> None:
    """Draw the menu, adjust to resize"""
    while True:
        if width != term.width or height != term.height or redraw:
            width = term.width
            height = term.height

            print(term.home + term.clear)

            horLine = "\u2550" * (width - 2)
            horLineTop = term.on_black("\u2554" + horLine + "\u2557")
            horLineBottom = term.on_black("\u255A" + horLine + "\u255D")
            horLineSep = term.on_black("\u2560" + horLine + "\u2563")
            vertLine = term.on_black("\u2551" + " " * (width - 2) + "\u2551")

            line = horLineTop + vertLine + horLineSep + vertLine * (height - 4) + horLineBottom

            print(term.home + term.clear + line + term.home)

            title = "Secretive Squirrels presents ..."
            set_text(term, 1, width // 2 - len(title) // 2, term.on_black(title))

            test = "  ____        _     ____            "
            test2 = " |  _ \\      | |   |  _ \\           "
            test3 = " | |_) | ___ | |__ | |_) | _____  __"
            test4 = " |  _ < / _ \\| '_ \\|  _ < / _ \\ \\/ /"
            test5 = " | |_) | (_) | |_) | |_) | (_) >  < "
            test6 = " |____/ \\___/|_.__/|____/ \\___/_/\\_\\"

            set_text(term, 5, width // 2 - len(test) // 2, term.on_black(test))
            set_text(term, 6, width // 2 - len(test2) // 2, term.on_black(test2))
            set_text(term, 7, width // 2 - len(test3) // 2, term.on_black(test3))
            set_text(term, 8, width // 2 - len(test4) // 2, term.on_black(test4))
            set_text(term, 9, width // 2 - len(test5) // 2, term.on_black(test5))
            set_text(term, 10, width // 2 - len(test6) // 2, term.on_black(test6))

            # welcome = "Welcome to BobBox!"
            # set_text(term, 5, width // 2 - len(welcome) // 2, term.on_black(welcome))
            # set_text(term, 0,0, str(term.get_location()[0]))

            if (height < optimal_height or width < optimal_width):
                error_screen = "BobBox says: Screen too small!"
                error_width = "Best width: " + str(optimal_width)
                error_cur_width = "Current width: " + str(width)
                error_height = "Best height: " + str(optimal_height)
                error_cur_height = "Current height: " + str(height)

                set_text(term, term.get_location()[0] + 1, width // 2 - len(error_screen) // 2,
                         term.on_red(error_screen))

                set_text(term, term.get_location()[0] + 1, width // 2 - len(error_width) // 2,
                         term.on_red(error_width) if width < optimal_width else term.on_green(error_width))
                set_text(term, term.get_location()[0], width // 2 - len(error_cur_width) // 2,
                         term.on_red(error_cur_width) if width < optimal_width else term.on_green(error_cur_width))

                set_text(term, term.get_location()[0] + 1, width // 2 - len(error_height) // 2,
                         term.on_red(error_height) if height < optimal_height else term.on_green(error_height))
                set_text(term, term.get_location()[0], width // 2 - len(error_cur_height) // 2,
                         term.on_red(error_cur_height) if height < optimal_height else term.on_green(error_cur_height))

            set_text(term, term.get_location()[0] + 3, 1, term.on_black(" "))
            for i in range(len(options)):
                options[i]['x'] = width // 2 - len(options[i]["text"]) // 2
                options[i]['y'] = term.get_location()[0]
                set_text(term, options[i]['y'], options[i]['x'], term.on_black(options[i]["text"]))

                set_text(term, options[i]['y'], options[i]['x'] - 2,
                         term.on_black("[" if options[i]['selected'] else " "))
                set_text(term, options[i]['y'], options[i]['x'] + len(options[i]["text"]) + 1,
                         term.on_black("]" if options[i]['selected'] else " "))
        await asyncio.sleep(0.01)


async def handle_inputs(term: object) -> None:
    """Handles the inputs for the options"""
    while True:
        key = term.inkey(timeout=0.1)
        if key.code == KEY_UP and not options[0]['selected']:
            for index, item in enumerate(options):
                if item['selected']:
                    item['selected'] = False
                    options[index - 1]['selected'] = True

                    set_text(term, item['y'], item['x'] - 2, term.on_black(" "))
                    set_text(term, item['y'], item['x'] + len(item["text"]) + 1, term.on_black(" "))
                    set_text(term, options[index - 1]['y'], options[index - 1]['x'] - 2, term.on_black("["))
                    set_text(term, options[index - 1]['y'],
                             options[index - 1]['x'] + len(options[index - 1]["text"]) + 1,
                             term.on_black("]"))
                    break

        if key.code == KEY_DOWN and not options[len(options) - 1]['selected']:
            for index, item in enumerate(options):
                if item['selected']:
                    item['selected'] = False
                    options[index + 1]['selected'] = True

                    set_text(term, item['y'], item['x'] - 2, term.on_black(" "))
                    set_text(term, item['y'], item['x'] + len(item["text"]) + 1, term.on_black(" "))
                    set_text(term, options[index + 1]['y'], options[index + 1]['x'] - 2, term.on_black("["))
                    set_text(term, options[index + 1]['y'],
                             options[index + 1]['x'] + len(options[index + 1]["text"]) + 1,
                             term.on_black("]"))
                    break

        if key.code == KEY_ENTER:
            for index, item in enumerate(options):
                if item['selected']:
                    if item['callback'] is not None:
                        item['callback'](term)
                        break

        await asyncio.sleep(0.01)


async def main() -> None:
    """Main function -- WIP"""
    pass


loop = asyncio.get_event_loop()
try:
    with term.fullscreen(), term.hidden_cursor(), term.cbreak(), term.keypad():
        asyncio.ensure_future(main())
        asyncio.ensure_future(draw_menu(term, width, height))
        asyncio.ensure_future(handle_inputs(term))
        loop.run_forever()

except KeyboardInterrupt:
    pass
finally:
    pass
