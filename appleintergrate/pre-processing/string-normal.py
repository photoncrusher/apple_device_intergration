# String normalizing
import json
import re
from transformer import transform
# normalize the key
def normalize_key(text):
    normal_text = text.lower()
    normal_text = re.sub(r'[^\w\s]','',normal_text)
    normal_text = re.sub(' +', ' ',normal_text)
    return normal_text

f = open('AppleDataIntergration\\apple_device_intergration\\appleintergrate\pre-processing\\fpt.json',)
data = json.load(f)
k = []

for a in data:
    for key in a.keys():
        transform(normalize_key(key))