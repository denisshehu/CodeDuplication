import json
import os

from DataModels import *

sorted_version_numbers = sorted(os.listdir('../jquery-data'))[:-1]
jQuery_versions = [JQueryVersion(item) for item in sorted_version_numbers]

for version in jQuery_versions:
    os.system('cloc --json --report-file=cloc_result.json ../jquery-data/' + version.version_number + '/src')

    with open('cloc_result.json') as json_file:
        version.add_lines_of_code(json.load(json_file)['JavaScript']['code'])

# for i in jQuery_versions:
#     print(i.version_number + ': ' + str(i.lines_of_code))

heatmap_cells = []

for i in range(1, len(jQuery_versions)):
    for j in range(i):
        heatmap_cells.append(HeatmapCell(jQuery_versions[i], jQuery_versions[j]))

# for cell in heatmap_cells:
#     print(cell.rowVersion.version_number + ': ' + cell.columnVersion.version_number)
