import csv
from collections import defaultdict

UPLOAD_FOLDER = "C:\\Kod\\Projekt\\handikapp_webpage\\uploads"


def read_csv(name, udisc):
    dict1 = defaultdict(list)

    with open(name, "r", encoding="utf-8") as score_card:
        for i in csv.reader(score_card):
            if udisc.lower() in i[0].lower():
                dict1[f"{i[1]} {i[2]}"].append(int(i[4]))
    return {key: dict1[key] for key in sorted(dict1)}


def sort_rounds(name):
    with open(f"{UPLOAD_FOLDER}\\{name}", "r", encoding="utf-8") as score_card:
        return [[f"{i[1]} {i[2]}", i[3], int(i[4])] for i in csv.reader(score_card) if name.lower()[:-4] in i[0].lower()]
