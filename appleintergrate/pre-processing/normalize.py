import re

def normalize(text):
    normal_text = text.lower()
    normal_text = re.sub(r'[^\w\s]','',normal_text)
    normal_text = re.sub(' +', ' ',normal_text)
    return normal_text
    