from methods import *

# get the jQuery version numbers present in the 'jquery_releases.csv' file
version_numbers = get_version_numbers()

# for i in version_numbers:
#     print(i)

# create a JQueryVersion object for every version number
jQuery_versions = [JQueryVersion(element) for element in version_numbers]

# get the lines of code of these jQuery versions
get_lines_of_code(jQuery_versions)

# compute the relative size of each jQuery version
compute_relative_sizes(jQuery_versions)

# for version in jQuery_versions:
#     print(version.get_version_number() + ': ' + str(version.get_relative_size()))

heatmap_cells = compute_heatmap_data(jQuery_versions)

# for cell in heatmap_cells:
#     print(cell.get_row_version().get_version_number() + ', ' + cell.get_column_version().get_version_number() + ': ' +
#           str(cell.get_coverage()))

dataframe = transform_into_dataframe(version_numbers, heatmap_cells)
plot_heatmap(dataframe)
# df.to_csv('heatmap_data.csv')
