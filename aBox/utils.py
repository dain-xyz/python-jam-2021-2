from rich import print
import json


def json_representation():
    """
    json uses character codes for example \u25a0 for the ■ symbol
    use this to convert characters to json format
    """
    while True:
        chars_to_convert = input("Characters to convert (or q to quit): ")
        if chars_to_convert == "q":
            break

        print(json.dumps(chars_to_convert))
