from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from collections import defaultdict

DRIVER_PATH = "C:\\Program Files (x86)\\Webdrivers\\chromedriver.exe"
PLAYER_PATH = "C:\\Kod\\Projekt\\Handicap system for Discgolf\\Player_data"


def download(event_link, headless=True):
    options = Options()
    options.headless = headless
    options.add_argument("--window-size=2000,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(event_link)
    score = [score.get_property("innerHTML") for score in driver.find_elements_by_class_name('round')]
    rating = [rating.get_property("innerHTML") for rating in driver.find_elements_by_class_name("player-rating")]
    return score, rating


def read_csv(name):
    dict1 = defaultdict(list)

    with open(f"{PLAYER_PATH}\\{name}.csv", "r", encoding="utf-8") as score_card:
        for i in csv.reader(score_card):
            if name.lower() in i[0].lower():
                dict1[f"{i[1]} {i[2]}"].append(int(i[4]))
    return {key: dict1[key] for key in sorted(dict1)}


def sort_rounds(name):
    with open(f"{PLAYER_PATH}\\{name}.csv", "r", encoding="utf-8") as score_card:
        return [[f"{i[1]} {i[2]}", i[3], int(i[4])] for i in csv.reader(score_card) if name.lower() in i[0].lower()]


def create_or_add_to_dict(dict2, course, name, i):
    if "Par" in i[0]:
        if dict2[course] == {}:
            dict2[course]["PAR"] = [int(i[4])]
            dict2[course].update({j: [int(i[j + 5]), []] for j in range(1, 19) if i[j + 5].isnumeric()})
    if name.lower() in i[0].lower():
        try:
            for j in range(1, 19):
                dict2[course][j][1].append(int(i[j + 5]))
        except KeyError:
            print(f"{course}: Hole {j} could not be processed")


def course_stats(name):
    dict2 = defaultdict(dict)
    with open(f"{PLAYER_PATH}\\{name}.csv", "r", encoding="utf-8") as score_card:
        for h, i in enumerate(csv.reader(score_card)):
            course = f"{i[1]} {i[2]}"
            create_or_add_to_dict(dict2, course, name, i)
    return dict2

