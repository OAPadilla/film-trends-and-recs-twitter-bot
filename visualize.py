import datetime
import re
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns


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
    plt.show()


def generate_rec_chart():
    pass

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

    data2 = [(3, 'Spider-Man: Into the Spider-Verse', '2018', 85603, 45177, '2019-01-18', 0),
            (2, 'The Favourite', '2018', 51138, 19661, '2019-01-18', 0),
            (1, 'Bird Box', '2018', 92460, 16528, '2019-01-18', 0),
            (8, 'Black Mirror: Bandersnatch', '2018', 72181, 16726, '2019-01-18', 0),
            (6, 'Roma', '2018', 65460, 25511, '2019-01-18', 6),
            (7, 'If Beale Street Could Talk', '2018', 15733, 5987, '2019-01-18', 0),
            (4, 'Aquaman', '2018', 55935, 14966, '2019-01-18', 0),
            (5, 'Vice', '2018', 20506, 3998, '2019-01-18', 0),

            (1, 'Spider-Man: Into the Spider-Verse', '2018', 85603, 45177, '2019-01-25', 3),
            (2, 'The Favourite', '2018', 51138, 19661, '2019-01-25', 2),
            (3, 'Bird Box', '2018', 92460, 16528, '2019-01-25', 1),
            (4, 'Black Mirror: Bandersnatch', '2018', 72181, 16726, '2019-01-25', 8),
            (5, 'Roma', '2018', 65460, 25511, '2019-01-25', 6),
            (6, 'If Beale Street Could Talk', '2018', 15733, 5987, '2019-01-25', 7),
            (7, 'Aquaman', '2018', 55935, 14966, '2019-01-25', 4),
            (8, 'Vice', '2018', 20506, 3998, '2019-01-25', 5),

            (2, 'Spider-Man: Into the Spider-Verse', '2018', 85603, 45177, '2019-02-01', 1),
            (1, 'The Favourite', '2018', 51138, 19661, '2019-02-01', 2),
            (8, 'Bird Box', '2018', 92460, 16528, '2019-02-01', 3),
            (4, 'Black Mirror: Bandersnatch', '2018', 72181, 16726, '2019-02-01', 4),
            (6, 'Roma', '2018', 65460, 25511, '2019-02-01', 5),
            (5, 'If Beale Street Could Talk', '2018', 15733, 5987, '2019-02-01', 6),
            (3, 'Aquaman', '2018', 55935, 14966, '2019-02-01', 7),
            (7, 'Vice', '2018', 20506, 3998, '2019-02-01', 8)
            ]

    generate_pop_film_chart(data1)