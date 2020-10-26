import pickle
import os
import glob
from collections import defaultdict
from settings.data_functions.handle_data import convert_ratings_to_dict

COURSE_DATA_PATH = "C:\\Kod\\Projekt\\Handicap system for Discgolf\\Course_data"
PLAYER_DATA_PATH = "C:\\Kod\\Projekt\\Handicap system for Discgolf\\Player_data"


def store_course_data(course_name, object1, object2, link="ALL_ROUNDS"):
    while True:
        try:
            with open(f"{COURSE_DATA_PATH}\\{course_name}\\{course_name} {link}.dat", "wb") as file:
                pickle.dump(object1, file)
                pickle.dump(object2, file)
                break
        except FileNotFoundError:
            os.makedirs(f"{COURSE_DATA_PATH}\\{course_name}")


def course_data(course_name):
    rating, score = [], []
    for path, sub_folder, file_list in os.walk(COURSE_DATA_PATH):
        for name in file_list:
            if course_name in name:
                with open(os.path.join(path, name), "rb") as file:
                    rating += pickle.load(file)
                    score += pickle.load(file)
    return rating, score


def store_player_data(player_name, object1):
    while True:
        try:
            with open(f"{PLAYER_DATA_PATH}\\{player_name}\\{player_name}.dat", "wb") as file:
                pickle.dump(object1, file)
                break

        except FileNotFoundError:
            os.makedirs(f"{PLAYER_DATA_PATH}\\{player_name}")


def get_file(name, path):
    with open(os.path.join(path, name), "rb") as file:
        return pickle.load(file)


def player_data(player_name):
    for path, sub_folder, file_list in os.walk(PLAYER_DATA_PATH):
        for name in file_list:
            if player_name in name:
                return get_file(name, path)


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


def store_hole_stats(data, name):
    with open(f"{COURSE_DATA_PATH}\\Hole_statistics\\{name}.dat", "wb") as file:
        pickle.dump(data, file)


def check_and_append(v, stats, k, stored_stats):
    for key, val in v.items():
        if not val == stats[k][key] and not key == "PAR":
            for num in stored_stats[k][key][1]:
                stats[k][key][1].append(num)


def get_stats_from_file(path, file, stats):
    with open(os.path.join(path, file), "rb") as stored:
        stored_stats = pickle.load(stored)
        for k, v in stored_stats.items():
            if k not in stats.keys():
                stats[k] = stored_stats[k]
            else:
                check_and_append(v, stats, k, stored_stats)


def load_hole_stats():
    stats = defaultdict()
    for path, sub_folder, file_list in os.walk(f"{COURSE_DATA_PATH}\\Hole_statistics"):
        for file in file_list:
            get_stats_from_file(path, file, stats)
    return stats


def list_courses():
    for path, sub_folder, file_list in os.walk(COURSE_DATA_PATH):
        return [folder for folder in sub_folder if not folder == "Hole_statistics"]


def search_course(name):
    return [name for path, fol_list, files in os.walk(COURSE_DATA_PATH) for folder in fol_list if name == folder]


def list_players(ranked=False):
    players = []
    if ranked:
        match = glob.glob(f'Player_data/*/*.dat')
        for i in match:
            with open(i, "rb") as file:
                players.append(pickle.load(file))
    else:
        for path, sub_folder, file_list in os.walk(PLAYER_DATA_PATH):
            return [folder for folder in sub_folder]
    return players


