from itertools import chain
import numpy as np


def filter_lists(clean_round, clean_rating):
    matched_rating = clean_rating[:len(clean_round) - (len(clean_rating) - len(clean_round))]
    rating = [matched_rating[i] for i, val in enumerate(matched_rating) if val != 0]
    score = [clean_round[i] for i, val in enumerate(matched_rating) if val != 0]
    rating = [rating[i] for i, val in enumerate(score) if 10 < val < 120]
    score = [score[i] for i, val in enumerate(score) if 10 < val < 120]

    return score, rating


def clean_raw_data(score, rating):
    clean_round = [int(i) for i in score if i.isnumeric()]
    clean_rating = list(filter(lambda x: x.isnumeric(), (map(lambda x: "0" if x == "" else x, rating))))
    clean_rating = list(chain.from_iterable([[int(i), int(i)] for i in clean_rating]))

    return filter_lists(clean_round, clean_rating)


def convert_ratings_to_dict(rating, score, calc_player=False):
    coef = np.polyfit(rating, score, 1)
    predicted_ratings = [i for i in range(500, 1200)]
    if calc_player:
        predicted = list(np.polyval(coef, predicted_ratings))
    else:
        predicted = list(map(int, np.polyval(coef, predicted_ratings)))

    return {predicted[i]: predicted_ratings[i] for i in range(len(predicted))}


def calc_average_by_hole(s):
    d = []
    index = 0
    for k, v in s.items():
        d.append([k])
        sub_index = 2
        for key, value in s[k].items():
            if key == "PAR":
                d[index].append(s[k][key])
            elif value != [0, []]:
                d[index].append([f"{key}:", s[k][key][0], round(sum(s[k][key][1]) / len(s[k][key][1]), 2)])
                diff = round(d[index][sub_index][2] - d[index][sub_index][1], 2)
                d[index][sub_index].append(diff)
                sub_index += 1
        index += 1
    return d


def sort_by_diff(s):
    res = []
    for i in s:
        temp = i[2:]
        temp.sort(key=lambda x: x[3], reverse=True)
        res.append(i[:2] + temp)
    return res
