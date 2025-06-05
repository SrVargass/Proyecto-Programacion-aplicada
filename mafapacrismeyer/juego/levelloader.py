import json
from clases import Level

levels = []
def add_level(filename):
    path = "niveles/"+filename
    with open(path, "r") as file:
        data = json.load(file)
        levels.append(data)

add_level("nivel_0.json")
add_level("nivel_1.json")
add_level("nivel_2.json")



def load_level(level_index):
    level = Level(levels[level_index])
    return level
