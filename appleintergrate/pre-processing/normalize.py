import re

def normalize_key(text):
    normal_text = text.lower()
    normal_text = re.sub(r'[^\w\s]','',normal_text)
    normal_text = re.sub(' +', ' ',normal_text)
    return normal_text

def normalize_data(data):
    new_data = []
    for i in data:
        if i != {}:
            new_data.append(i)
    norm_data = new_data
    for i in new_data:
        for key in i.keys():
            i[key] = i[key].split(",")
    return norm_data
    