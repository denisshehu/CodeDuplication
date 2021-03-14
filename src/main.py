from methods import *

# get the jQuery version numbers present in the 'jquery_releases.csv' file
version_numbers = get_version_numbers()

# for i in version_numbers:
#     print(i)

# create a JQueryVersion object for every version number
jQuery_versions = [JQueryVersion(element) for element in version_numbers]

# get the lines of code of these jQuery versions
get_lines_of_code(jQuery_versions)

# Copy the versions loc info to data.json file for later usage
versions_dict = {}
for i in jQuery_versions:
    versions_dict[i.version_number] = str(i.lines_of_code)
    # print(i.version_number + ': ' + str(i.lines_of_code))
jsonString = json.dumps(versions_dict)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
#

heatmap_cells = compute_heatmap_data(jQuery_versions)

# for cell in heatmap_cells:
#     print(cell.get_row_version().get_version_number() + ', ' + cell.get_column_version().get_version_number() + ': ' +
#           str(cell.get_coverage()))

df = transform_into_dataframe(version_numbers, heatmap_cells)
df.to_csv('heatmap_data.csv')
