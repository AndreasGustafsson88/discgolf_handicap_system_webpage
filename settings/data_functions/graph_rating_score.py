import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np


def plot_data(rating, score, course, color="Blue", x_label="RATING", y_label="SCORE"):

    plt.scatter(rating, score, color=color)

    coef = np.polyfit(rating, score, 1)
    predicted_ratings = [i for i in range(650, 1080)]
    predicted = np.polyval(coef, predicted_ratings)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(course)
    plt.plot(predicted_ratings, predicted, lw=2, color="Black")

    plt.show()


def plot_player(name, data, x_label="TIME", y_label="RATING"):

    date = [datetime.strftime(datetime.strptime(i[0], "%Y-%m-%d %H:%M"), "%Y-%m-%d") for i in data]
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.plot(date, [i[1] for i in data])
    plt.gcf().autofmt_xdate()
    plt.gca().set_ylim([650, 1100])
    plt.gca().invert_xaxis()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(name)

    plt.show()

