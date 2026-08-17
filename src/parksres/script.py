import json

with open(PARKS_SOURCE) as file:  
    data = json.load(file)
print(len(data))