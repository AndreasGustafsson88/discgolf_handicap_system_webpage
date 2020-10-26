import csv
import pickle
import statistics
from collections import defaultdict

import numpy as np

from settings import *
import os

UPLOAD_FOLDER = "C:\\Kod\\Projekt\\handikapp_webpage\\uploads"


def sort_rounds(name, udisc):
    with open(name, "r", encoding="utf-8") as score_card:
        return [[f"{i[1]} {i[2]}", i[3], int(i[4])] for i in csv.reader(score_card) if udisc.lower() in i[0].lower()]


def read_csv(name, udisc):
    dict1 = defaultdict(list)

    with open(name, "r", encoding="utf-8") as score_card:
        for i in csv.reader(score_card):
            if udisc.lower() in i[0].lower():
                dict1[f"{i[1]} {i[2]}"].append(int(i[4]))
    return {key: dict1[key] for key in sorted(dict1)}


def list_courses():
    for path, sub_folder, file_list in os.walk(COURSE_DATA_PATH):
        return [folder for folder in sub_folder if not folder == "Hole_statistics"]


def calc_rating(scores, rounds=20, course=""):
    rating, rounds = get_rating(scores, rounds, course)
    player_rating = int(statistics.mean(rating))
    return player_rating, rounds


def convert_ratings_to_dict(rating, score, calc_player=False):
    coef = np.polyfit(rating, score, 1)
    predicted_ratings = [i for i in range(500, 1200)]
    if calc_player:
        predicted = list(np.polyval(coef, predicted_ratings))
    else:
        predicted = list(map(int, np.polyval(coef, predicted_ratings)))

    return {predicted[i]: predicted_ratings[i] for i in range(len(predicted))}


def add_to_list(all_rating, ratings, values, how_many_rounds, file):
    average = convert_ratings_to_dict(pickle.load(file), pickle.load(file))
    if all_rating:
        try:
            ratings.append([values[1], average[values[2]]])
        except KeyError:
            print(f"{values} round either rated too low or too high, must be between 500 or 1200")
    else:
        try:
            ratings.append(average[values[2]])
            how_many_rounds.append(0)
        except KeyError:
            print(f"{values} round either rated too low or too high, must be between 500 or 1200")


def check_match(values, course, all_rating, ratings, how_many_rounds):
    for path, sub_folder, file_list in os.walk(COURSE_DATA_PATH):
        for name in file_list:
            if values[0] in name and "ALL_ROUNDS" in name and course in name:
                with open(os.path.join(path, name), "rb") as file:
                    add_to_list(all_rating, ratings, values, how_many_rounds, file)


def get_rating(player_scores, rounds, course, all_rating=False):
    ratings = []
    how_many_rounds = []
    for values in player_scores:
        if len(how_many_rounds) == rounds:
            return ratings, len(how_many_rounds)
        check_match(values, course, all_rating, ratings, how_many_rounds)
    return ratings, len(how_many_rounds)
