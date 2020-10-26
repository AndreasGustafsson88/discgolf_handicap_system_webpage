import re
from settings.data_functions.get_ext_data import course_stats
from settings.data_functions.graph_rating_score import plot_player, plot_data
from settings.data_functions.handle_data import convert_ratings_to_dict, calc_average_by_hole, sort_by_diff
from settings.data_functions.save_and_load import store_hole_stats, load_hole_stats, player_data, course_data, get_rating, \
    list_courses, list_players


class Database:
    def __init__(self, name):
        self.name = name
        self.hole_stats = []
        self.courses = []
        self.players = []
        self.hole_difficulty = []

    @staticmethod
    def plot_course(name):
        rating, score = course_data(name)
        plot_data(rating, score, name)

    @staticmethod
    def load_player(full_name):
        return player_data(full_name)

    def get_throws(self, player_rating, course):
        rating, score = course_data(course)
        score_dict = convert_ratings_to_dict(rating, score, calc_player=True)
        throws = [int(round(k)) for k, v in score_dict.items() if player_rating == v]
        for i in self.hole_difficulty:
            if course in re.sub("[:]", "", i[0]):
                difference = throws[0] - i[1][0]
                if difference > 18:
                    new_diff = difference - 18
                    holes = [int(i[j][0][:-1]) for j in range(2, new_diff + 2)]
                    return holes, i[1][0], difference
                elif difference > 0:
                    holes = [int(i[j][0][:-1]) for j in range(2, difference + 2)]
                    return holes, i[1][0], difference
                elif difference < 0:
                    holes = [int(i[j][0][:-1]) for j in range(-1, difference - 1, -1)]
                    return holes, i[1][0], difference
                elif difference == 0:
                    return None, i[1][0], difference

    def player_history(self, name, course=""):
        player = self.load_player(name)
        rating_date, _ = get_rating(player.player_scores, 20, course, all_rating=True)
        plot_player(name, rating_date)

    def get_hole_average(self, sort=True, course="ALL"):
        self.hole_difficulty = calc_average_by_hole(self.hole_stats)
        if not course == "ALL":
            result = [self.hole_difficulty[i] for i, eni in enumerate(self.hole_difficulty) if course == eni[0]]
            print(result)
            return
        if sort:
            self.hole_difficulty = sort_by_diff(self.hole_difficulty)
        print("\n".join(f"{i}" for i in sorted(self.hole_difficulty)))

    def all_overview(self, file_name, show=True):
        self.hole_stats = course_stats(file_name)
        print("\n".join(f"{key}: {self.hole_stats[key]}" for key in self.hole_stats.keys() if show))
        return self.hole_stats

    def store_hole_overview(self, name):
        store_hole_stats(self.hole_stats, name)
        print("Save successful")

    def update_database(self):
        self.hole_stats = load_hole_stats()
        self.hole_difficulty = sort_by_diff(calc_average_by_hole(self.hole_stats))
        self.courses = list_courses()
        self.players = list_players()
        print("database updated successfully")

    def save_database(self):
        pass

    def show_courses(self):
        print(f"There's a total of {len(self.courses)} courses and layouts currently in the database")
        print("\n".join(f"{i}: {eni}" for i, eni in enumerate(self.courses, 1)))

    def show_players(self, ranked=False):
        if ranked:
            player = list_players(ranked=True)
            print(f"There's a total of {len(self.players)} players currently in the database")
            for j, i in enumerate(player, 1):
                print(f"{j}: {i.full_name}, {i.rating}")
        else:
            print(f"There's a total of {len(self.players)} players currently in the database")
            print("\n".join(f"{i}: {eni}" for i, eni in enumerate(self.players, 1)))

