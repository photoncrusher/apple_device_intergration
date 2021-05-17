# String normalizing
import json
import re
from transformer import transform
from normalize import normalize_key, normalize_data
# normalize the key

f = open('AppleDataIntergration\\apple_device_intergration\\appleintergrate\pre-processing\\fpt.json',)
data = json.load(f)
k = []
for a in data:
    for key in a.keys():
        k.append(key)
k = set(k)
data = normalize_data(data)
print(data)
# with open('AppleDataIntergration\\apple_device_intergration\\appleintergrate\pre-processing\\fpt.json', 'wb+') as outfile:
#     json.dump(data, outfile)