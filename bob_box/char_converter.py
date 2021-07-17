from rich import print
import json
chars_toconvert = input("Characters to convert: ")
print(json.dumps(chars_toconvert))
"""
json uses character codes for example \u25a0 for the ■ symbol
use this to convert characters to json format
"""