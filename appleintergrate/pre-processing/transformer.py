from os import stat
import scrapy
from string_matching import levenshtein_ratio_and_distance
def transform(text):
    types = ["types","loại"]
    name = ["name","tên"]
    screen = ["screen","màn hình", "tấm nền"]
    CPU = ["cpu", "vi xử lý"]
    ROM = ["rom", "bộ nhớ trong"]
    RAM = ["ram"]
    rear_cam = ["rear_cam","camera sat", "camera chính", "cam sau"]
    front_cam = ["front_cam","camera trước", "camera selfie", "cam trước"]
    SIM = ["sim","thẻ sim"]
    security = ["security","bảo mật"]
    weigth = ["weigth","trọng lượng", "cân nặng"]
    operatingsys = ["operatingsys","hệ điều hành"]
    warranty = ["warranty","bảo hành"]
    status = ["status","trạng thái"]
    price = ["price","giá"]
    available = ["available"]
    feature_list = [types,name,screen,CPU,ROM,RAM,rear_cam,front_cam,SIM,security,weigth,operatingsys,warranty,status,price,available]
    for feature in feature_list:
        for num in range(len(feature)):
            Distance = levenshtein_ratio_and_distance(text,feature[num],ratio_calc = True)
            if Distance >= 0.8:
                text = feature[0]
    return text