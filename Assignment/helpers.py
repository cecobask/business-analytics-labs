import seaborn
import matplotlib.pyplot as plt
import numpy


def parents_type(row):
    """
    Determine if the parents are bossy or soft.
    The questions asked are of format: Do your parents let you make your own decisions about...
    Possible answers are:
    0 -- no
    1 -- yes
    A parent is considered soft if they let their child make their own decisions about 4 or more questions (out of 7).
    :param row: Series
    :return: bool
    """
    # Create a dictionary with unique values (1 and 0) and their counts.
    unique, counts = numpy.unique(row.values, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    yes_answers = counts_dict.get(1, 0)  # Get the number of 'yes' answers or replace with 0 if missing.
    return 'Soft' if yes_answers > 4 else 'Bossy'


def show_axis_percentages(plot, column):
    """
    Helper function that adds percentages to the right of horizontal plot bars.
    :param plot: AxesSubplot
    :param column: Series
    :return: None
    """
    for p in plot.patches:
        percentage = '{:.1f}%'.format(100 * p.get_width() / column.value_counts().sum())
        x = p.get_x() + p.get_width() + 0.02
        y = p.get_y() + p.get_height() / 2
        plot.annotate(percentage, (x, y))


def parents_edu_level(row):
    """
    Determines the average education level of the parents.
    :param row: Series
    :return: numpy.float64
    """
    mother = row['H1RM1']
    father = row['H1RF1']

    return (mother + father) / 2


def parents_child_bond(row):
    """
    Calculates how close children are with their parents and how much they think their parents care about them.
    The results of these two calculations is used to determine a bond score.
    Values indicate:
    #1 not at all
    #2 very little
    #3 somewhat
    #4 quite a bit
    #5 very much
    :param row: Series
    :return: numpy.float64
    """
    mother2child = row['H1WP10']
    father2child = row['H1WP14']
    child2mother = row['H1WP9']
    child2father = row['H1WP13']

    # Calculate individual affinities first.
    parents2child = (mother2child + father2child) / 2
    child2parents = (child2mother + child2father) / 2

    return (parents2child + child2parents) / 2


def rename_h1to1(row):
    """
    Replaces floats with readable string values for display purposes.
    :param row: float64
    :return: str
    """
    if row == 0:
        return 'NO'
    else:
        return 'YES'


def build_countplot(dataset, column_name, title, ylabel, xlabel='FREQUENCY'):
    """
    Abstract the creation and showing of countplot, as it is heavily used
    for my research questions, due to their categorical nature.
    :param dataset: DataFrame
    :param column_name: str
    :param title: str
    :param ylabel: str
    :param xlabel: str
    :return: None
    """
    plt.figure(figsize=(7.5, 4.8))
    ax = seaborn.countplot(y=column_name, data=dataset)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    show_axis_percentages(ax, dataset[column_name])
    plt.show()