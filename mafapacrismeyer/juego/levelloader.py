import json
import os
from clases import Level

levels = []
def add_level(filename):
    #path = os.path.join(os.path.dirname(__file__)+"/niveles/"+filename
    path = os.path.join(os.path.dirname(__file__), 'niveles', filename)
    with open(path, "r") as file:
        data = json.load(file)
        levels.append(data)

path = os.path.join(os.path.dirname(__file__), 'niveles')
fileArray = os.listdir(path)
fileArray.sort()

for filename in fileArray:
    add_level(filename)
    
#add_level("nivel_0.json")
#add_level("nivel_1.json")
#add_level("nivel_2.json")
#add_level("nivel_3.json")
#add_level("nivel_4.json")
#add_level("nivel_5.json")
#add_level("nivel_6.json")

print(fileArray)

def load_level(level_index, colorHue=55):
    index = level_index % len(fileArray) #
    
    level = Level(levels[index], colorHue=colorHue) #
    return level
