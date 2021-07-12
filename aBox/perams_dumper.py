import json

objects = [
    {'ob': 'air', 'r': 255, 'g': 255, 'b': 255, 'char': ' '},
    {'ob': 'wall', 'r': 0, 'g': 0, 'b': 0, 'char': '█'},
    {'ob': 'player', 'r': 0, 'g': 162, 'b': 232, 'char': 'O'},
    {'ob': 'box', 'r': 255, 'g': 127, 'b': 39, 'char': '■'},
    {'ob': 'enemy', 'r': 237, 'g': 28, 'b': 36, 'char': 'X'},
    {'ob': 'fire', 'r': 136, 'g': 0, 'b': 21, 'char': '🔥'}
]

with open('objects.json', 'w') as json_file:
  json.dump(objects, json_file)