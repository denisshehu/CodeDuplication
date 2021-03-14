import csv
import os
import json

import pandas as pd

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

    # the version numbers are stored in decreasing order in the .csv file
    # thus the reverse of the current list must be returned
    answer.reverse()

    return answer


def get_lines_of_code(j_query_versions):
    """
    This method calls 'cloc' on every element of {:param j_query_versions} to get the number of lines of code of
    the jQuery version represented by that element. Only the files inside directory 'src' are included.

    :param j_query_versions: a list of JQueryVersion objects, each representing a jQuery version

    After execution, the attribute 'lines_of_code' of every JQueryVersion object in {:param j_query_versions}
    stores the lines of code of the jQuery version it represents.
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


def get_code_clones(heatmap_cell):
    """
    This method calls 'jsinspect' to report the duplicate lines of code between the two jQuery versions
    that are represented by the 'row_version' and 'column_version' attributes of {:param: heatmap_cell}.

    :param heatmap_cell: a HeatmapCell object
    :return: a json object storing the results of 'jsinspect'
    """

    # an error is reported when 'jsinspect' parses files intro.js and outro.js, thus they are ignored
    os.system('jsinspect -I -r json --ignore "intro|outro" ../jquery-data/' +
              heatmap_cell.get_row_version().get_version_number() + '/src ../jquery-data/' +
              heatmap_cell.get_column_version().get_version_number() + '/src > jsinspect_result.json')

    with open('jsinspect_result.json') as json_file:
        answer = json.load(json_file)

    return answer


def extract_json(code_clones):
    """

    :param code_clones:
    :return:
    """

    data = []
    unique_ids = []

    for match in code_clones:

        if not (match['id'] in unique_ids):
            unique_ids.append(match['id'])

            for instance in match['instances']:

                path = instance['path']
                index = -1

                for i in range(len(data)):
                    if path == data[i][0].get_path():
                        index = i
                        break

                if index == -1:
                    data.append([
                        JsInspectInstance(path, instance['lines'][0], instance['lines'][1])
                    ])
                else:
                    data[index].append(JsInspectInstance(path, instance['lines'][0], instance['lines'][1]))

    for instances_list in data:
        instances_list.sort(key=lambda x: x.starting_index)

    return data


def get_clones_lines_of_code(instances_list):
    """

    :param instances_list:
    :return:
    """

    answer = 0

    for i in range(len(instances_list)):

        instance = instances_list[i]

        if i == len(instances_list) - 1:
            answer += instance.get_ending_index() - instance.get_starting_index() + 1
        else:

            next_instance = instances_list[i + 1]

            if instance.get_ending_index() < next_instance.get_starting_index():
                answer += instance.get_ending_index() - instance.get_starting_index() + 1
            else:
                answer += next_instance.get_starting_index() - instance.get_starting_index()

    return answer


def compute_heatmap_data(j_query_versions):
    """

    :param j_query_versions:
    :return:
    """

    answer = []

    for i in range(1, len(j_query_versions)):  # range(1, 10):  # range(1, len(j_query_versions)):
        for j in range(i):
            heatmap_cell = HeatmapCell(j_query_versions[i], j_query_versions[j])

            code_clones = get_code_clones(heatmap_cell)

            data = extract_json(code_clones)

            clones_lines_of_code = 0

            for instances_list in data:
                clones_lines_of_code += get_clones_lines_of_code(instances_list)

            heatmap_cell.set_clones_lines_of_code(clones_lines_of_code)
            heatmap_cell.compute_coverage()

            print(heatmap_cell.get_row_version().get_version_number() + ', ' +
                  heatmap_cell.get_column_version().get_version_number() + ': ' +
                  str(heatmap_cell.get_coverage()))

            answer.append(heatmap_cell)

    return answer


def transform_into_dataframe(version_numbers, heatmap_cells):
    data = []
    index = 0

    for i in range(len(version_numbers)):
        row = []

        for j in range(len(version_numbers)):

            # if i < 10:
            if j >= i:
                row.append(0.0)
            else:
                row.append(heatmap_cells[index].get_coverage())
                index += 1
            # else:
            #     row.append(0.0)

        data.append(row)

    return pd.DataFrame(data=data, index=version_numbers, columns=version_numbers)
