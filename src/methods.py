import csv
import os
import json

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from data_models import *


def get_version_numbers():
    """
    This method loads and returns the version numbers from the column 'tag' of file 'jquery_releases.csv'
    in their order of release.

    :return: a list of strings representing the version numbers of jQuery
    """

    answer = []

    with open('../jquery-data/jquery_releases.csv', mode='r') as csv_file:
        content = csv.DictReader(csv_file)
        for row in content:
            answer.append(row['tag'])

    # the version numbers are stored in decreasing order in the .csv file,
    # thus the reverse of the current list must be returned
    answer.reverse()

    return answer


def get_lines_of_code(j_query_versions):
    """
    This method calls 'cloc' on every element of {:param j_query_versions} to get the number of lines of code of
    the jQuery version represented by that element. Only the files inside directory 'src'
    (excluding directory 'test' if present) are included.
    After execution, the attribute 'lines_of_code' of every JQueryVersion object in {:param j_query_versions}
    stores the lines of code of the jQuery version it represents.

    :param j_query_versions: a list of JQueryVersion objects, each representing a jQuery version
    """

    for version in j_query_versions:
        # files intro.js and outro.js if present in the jQuery version are excluded because when they are parsed
        # by 'jsinspect' an error is reported
        os.system('cloc --fullpath --not-match-f="intro|outro" --exclude-dir test --quiet --json ' +
                  '--report-file=cloc_result.json  ../jquery-data/' + version.get_version_number() + '/src')

        with open('cloc_result.json') as json_file:
            java_script_result = json.load(json_file)['JavaScript']

            # other than code, comments and blank lines are considered as lines of code
            version.set_lines_of_code(
                java_script_result['blank'] + java_script_result['comment'] + java_script_result['code'])

    pass


def compute_relative_sizes(j_query_versions):
    """
    This method computes the relative sizes of every element of {:param j_query_versions}. The relative size of a
    jQuery version is the ratio between its number of lines of code and the sum of the number of lines of code
    of every version in {:param j_query_versions}.

    :param j_query_versions: a list of JQueryVersion objects
    """

    total_lines_of_code = 0

    # compute the total number of lines of code
    for version in j_query_versions:
        total_lines_of_code += version.get_lines_of_code()

    for version in j_query_versions:
        # compute the relative size of the jQuery version
        relative_size = version.get_lines_of_code() / total_lines_of_code

        # set the attribute 'relative_size' to the value computed above
        version.set_relative_size(relative_size)

    pass


def get_code_clones(heatmap_cell):
    """
    This method calls 'jsinspect' to report the duplicate lines of code between the two jQuery versions
    that are represented by the 'row_version' and 'column_version' attributes of {:param: heatmap_cell}.

    :param heatmap_cell: a HeatmapCell object
    :return: a json object storing the results of 'jsinspect'
    """

    # an error is reported when 'jsinspect' parses files intro.js and outro.js, thus they are ignored
    os.system('jsinspect -I -r json --ignore "intro|outro|test" ../jquery-data/' +
              heatmap_cell.get_row_version().get_version_number() + '/src ../jquery-data/' +
              heatmap_cell.get_column_version().get_version_number() + '/src > jsinspect_result.json')

    with open('jsinspect_result.json') as json_file:
        answer = json.load(json_file)

    return answer


def extract_json(code_clones):
    """
    This method converts the json object returned by 'jsinspect' into a matrix of JsInspectInstance object.
    The matrix is constructed in such a way that instances referring to the same file are stored in the same list,
    thus each list represents the duplicate portions of a single file between the two different versions of jQuery.
    The json object might include duplicates, but these are ignored.

    :param code_clones: a json object returned by function {:func:`get_code_clones`}
    :return: a matrix of JsInspectInstance objects representing {:param code_clones}
    """

    data = []
    unique_ids = []

    for match in code_clones:

        # only consider those matches that have not been seen before, i.e. ignore duplicates
        if not (match['id'] in unique_ids):
            unique_ids.append(match['id'])

            for instance in match['instances']:

                # path of the file on which the duplicate code is
                path = instance['path']
                index = -1

                # check whether the list representing this file already exists in the matrix
                for i in range(len(data)):
                    if path == data[i][0].get_path():
                        # the list exists, so let index be the position of this list in the matrix
                        index = i
                        break

                if index == -1:
                    # the list does not exist, so a new list is added to the matrix
                    # and the current instance is added to it
                    data.append([
                        JsInspectInstance(path, instance['lines'][0], instance['lines'][1])
                    ])
                else:
                    # the list already exists, so add the current instance to it
                    data[index].append(JsInspectInstance(path, instance['lines'][0], instance['lines'][1]))

    # sort the elements of every list in a non-decreasing order based on which line of code the duplicated code starts
    for instances_list in data:
        instances_list.sort(key=lambda x: x.starting_index)

    return data


def get_clones_lines_of_code(instances_list):
    """
    This method computes the number of duplicated lines of code between two jQuery versions using
    {:param instances_list}, which is one of the lists of the matrix returned by {:func:`extract_json`}.
    
    :param instances_list: a list of JsInspectInstance object (a preprocessed representation of the 'jsinspect' result
                           on a single file)
    :return: the total number of duplicate lines of code in the file represented by {:param instances_list}
    """

    answer = 0

    for i in range(len(instances_list)):

        instance = instances_list[i]
        
        # an instance is either not the last one in the list, and thus its range of lines of code might overlap
        # with the next instance on the list, or it is the last one and there is no possible overlap

        if i == len(instances_list) - 1:
            # the current instance is the last one, so add all its lines of code to the total
            answer += instance.get_ending_index() - instance.get_starting_index() + 1
        else:
            # next instance in the list
            next_instance = instances_list[i + 1]

            if instance.get_ending_index() < next_instance.get_starting_index():
                # the instances do not overlap, so add all the lines of code of the current instance to the total
                answer += instance.get_ending_index() - instance.get_starting_index() + 1
            else:
                # the instances overlap, so add to the total the lines of code of the current instance until
                # the beginning of the next instance
                answer += next_instance.get_starting_index() - instance.get_starting_index()

    return answer


def compute_heatmap_data(j_query_versions):
    """
    This method computes and returns the coverage values for every pair of elements in {:param j_query_versions}.
    
    :param j_query_versions: a list of JQueryVersion objects
    :return: a list of HeatmapCell objects, each representing a cell of the heatmap
    """

    answer = []

    for i in range(1, len(j_query_versions)):
        for j in range(i):
            
            # single cell of the heatmap
            heatmap_cell = HeatmapCell(j_query_versions[i], j_query_versions[j])
            
            # the json object returned by 'jsinspect' on the current two jQuery versions
            code_clones = get_code_clones(heatmap_cell)
            
            # process and transform the json object into a matrix of JsInspectInstance objects
            data = extract_json(code_clones)

            clones_lines_of_code = 0
            
            # compute the duplicate lines of code between the current two jQuery versions
            for instances_list in data:
                clones_lines_of_code += get_clones_lines_of_code(instances_list)
            
            # set the cell's number of duplicate lines of code to the computed value
            heatmap_cell.set_clones_lines_of_code(clones_lines_of_code)

            # compute the coverage between the current two jQuery versions
            heatmap_cell.compute_coverage()

            print(heatmap_cell.get_row_version().get_version_number() + ', ' +
                  heatmap_cell.get_column_version().get_version_number() + ': ' +
                  str(heatmap_cell.get_coverage()))
            
            answer.append(heatmap_cell)

    return answer


def transform_into_dataframe(version_numbers, heatmap_cells):
    """
    This method transforms {:param heatmap_cells} into a pandas DataFrame.

    :param version_numbers: a list of jQuery version numbers,
                            its elements will be used as row and column names for the dataframe
    :param heatmap_cells: a list of HeatmapCell objects, each representing a single cell of the heatmap
    :return: a pandas DataFrame representation of the heatmap
    """

    data = []
    index = 0

    for i in range(len(version_numbers)):
        row = []

        for j in range(len(version_numbers)):

            if j >= i:
                # the upper triangle of the heatmap is not used
                row.append(0.0)
            else:
                row.append(heatmap_cells[index].get_coverage())
                index += 1

        data.append(row)

    return pd.DataFrame(data=data, index=version_numbers, columns=version_numbers)


def plot_heatmap(dataframe):
    """
    This method generates the heatmap corresponding to the pandas DataFrame {:param dataframe} and stores it as
    'heatmap.png' on the current directory.

    :param dataframe: a pandas DataFrame
    """

    fig, ax = plt.subplots(figsize=(14, 14))

    # define the color scheme of the heatmap
    colors = ['white', 'deepskyblue', 'forestgreen', 'yellow', 'red']
    color_map = LinearSegmentedColormap.from_list('color_map', colors)
    im = ax.imshow(dataframe, color_map, vmin=0.0, vmax=1.0)

    # add a color bar
    color_bar = ax.figure.colorbar(im, ax=ax)
    color_bar.ax.tick_params(labelsize=17)

    # add all possible ticks
    ax.set_xticks(np.arange(len(dataframe.columns)))
    ax.set_yticks(np.arange(len(dataframe.columns)))
    ax.tick_params(length=0)

    # label the ticks according to the row and column names of the dataframe
    ax.set_xticklabels(dataframe.columns)
    ax.set_yticklabels(dataframe.columns)
    plt.setp(ax.get_xticklabels(), rotation=90)

    # add a grid to the heatmap
    ax.set_xticks(np.arange(-0.5, len(dataframe.columns), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(dataframe.columns), 1), minor=True)
    ax.grid(which='minor', color='black', linewidth=2)

    fig.tight_layout()
    plt.savefig('heatmap.png')

    pass
