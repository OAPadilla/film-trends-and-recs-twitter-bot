import os
import datetime
import re
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import squarify
from tmdb_api import TheMovieDatabaseAPI
from secrets import *


POP_IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images', 'temp_pop.png')
RECS_IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images', 'temp_recs.png')

params = {'axes.titlesize': 22,
          'legend.fontsize': 16,
          'figure.figsize': (16, 10),
          'axes.labelsize': 16,
          'xtick.labelsize': 16,
          'ytick.labelsize': 16,
          'figure.titlesize': 22}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def generate_pop_film_chart(data):

    pop_df = pd.DataFrame(data, columns=['Rank', 'Title', 'Year', 'Watches', 'Likes', 'Date', 'Previous Rank'])

    # Draws new lines
    def newline(p1, p2):
        ax = plt.gca()
        if p1[1] != 0:
            l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color='green' if p1[1] - p2[1] >= 0 else 'red',
                              marker='o', markersize=6)
        else:
            l = mlines.Line2D([p2[0], p2[0]], [p2[1], p2[1]], color='gold', marker='s', markersize=6)
        ax.add_line(l)
        return l

    fig, ax = plt.subplots(1, 1, figsize=(9, 6), dpi=80)

    # Vertical lines
    ax.vlines(x=0.1, ymin=0, ymax=9, color='black', alpha=0.7, linewidth=1, linestyles='dotted')
    ax.vlines(x=1, ymin=0, ymax=9, color='black', alpha=0.7, linewidth=1, linestyles='dotted')

    # Line segments
    for pr, r, t, y in zip(pop_df['Previous Rank'], pop_df['Rank'], pop_df['Title'], pop_df['Year']):
        newline([0.1, pr], [1, r])
        ax.text(1.25-0.05, r, t + ' (' + y + ')', horizontalalignment='left', verticalalignment='center',
                fontdict={'size': 20})

    # Dates of last week
    match = re.search(r'\d{4}-\d{2}-\d{2}', str(pop_df['Date']))
    today_dt = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
    week_ago_dt = today_dt - datetime.timedelta(days=7)
    today = str(today_dt)[5:7] + '/' + str(today_dt)[8:]
    week_ago = str(week_ago_dt)[5:7] + '/' + str(week_ago_dt)[8:]

    # Labels
    ax.set_title("Popular Films of the Week ({}-{})".format(week_ago, today),
                 fontdict={'size': 32})
    ax.set(xlim=(0, 4), ylim=(8.5, 0.5), ylabel='Rank')
    ax.set_xticks([0.1, 1])
    ax.set_xticklabels(["Last Week\n" + week_ago, "Today\n" + today])
    plt.xticks(fontsize=12)
    plt.yticks()

    # Borders and display
    plt.gca().spines["top"].set_alpha(.0)
    plt.gca().spines["bottom"].set_alpha(.0)
    plt.gca().spines["right"].set_alpha(.0)
    plt.gca().spines["left"].set_alpha(.0)
    # plt.show()
    fig.savefig(POP_IMAGE_DIR)


def generate_rec_chart(data):

    rec_df = pd.DataFrame(data, columns=['Movie_id', 'Title', 'Date', 'Count'])

    # Download movie posters
    # m = TheMovieDatabaseAPI(TMDB_API_KEY)
    # for idx, m_id in enumerate(rec_df['Movie_id'], start=1):
    #     filename = "poster_top{}.png".format(str(idx))
    #     directory = os.path.join(os.path.dirname(__file__), 'images', filename)
    #     m.download_movie_poster(m_id, directory)

    # Use posters in plot

    # Prepare data
    num_films_display = 10
    years = ['(' + rec_df['Date'][x][:4] + ')' for x in range(num_films_display)]
    labels = [(rec_df['Title'][x] + '\n' + years[x]) for x in range(num_films_display)]
    sizes = rec_df['Count'].values.tolist()[:num_films_display]
    colors = ["#90aeae", "#a0c2c2", "#a9c8c8", "#b3cece", "#bcd4d4",
              "#c6dada", "#cfe0e0", "#d9e6e6", "#e2ecec", "#ecf2f2"]

    # Plot
    plt.figure(figsize=(12, 8), dpi=80)
    plt.figure = squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)

    # Borders and display
    plt.title("Recommended Films")
    plt.axis('off')
    # plt.show()
    plt.savefig(RECS_IMAGE_DIR)


if __name__ == '__main__':
    data1 = [
        (1, 'Spider-Man: Into the Spider-Verse', '2018', 85603, 45177, '2019-01-25', 3),
        (2, 'The Favourite', '2018', 51138, 19661, '2019-01-25', 2),
        (3, 'Bird Box', '2018', 92460, 16528, '2019-01-25', 1),
        (4, 'Black Mirror: Bandersnatch', '2018', 72181, 16726, '2019-01-25', 8),
        (5, 'Roma', '2018', 65460, 25511, '2019-01-25', 6),
        (6, 'If Beale Street Could Talk', '2018', 15733, 5987, '2019-01-25', 0),
        (7, 'Aquaman', '2018', 55935, 14966, '2019-01-25', 4),
        (8, 'Vice', '2018', 20506, 3998, '2019-01-25', 5),
    ]

    data2 = [
        (4347, 'Atonement', "1998-07-10", 16),
        (4995, 'Boogie Nights', "1998-07-10", 3),
        (49047, 'Gravity', "1998-07-10", 2),
        (8051, 'Punch-Drunk Love', "1998-07-10", 1),
        (1391, 'Y Tu Mamá También', "1998-07-10", 1),
        (103731, 'Mud', "1998-07-10", 1),
        (12573, 'A Serious Man', "1998-07-10", 1),
        (44264, 'True Grit', "1998-07-10", 1),
        (75, 'Mars Attacks!', "1998-07-10", 1),
        (473, 'Pi', "1998-07-10", 1)
    ]

    # generate_pop_film_chart(data1)
    generate_rec_chart(data2)
