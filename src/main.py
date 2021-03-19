from methods import *

# get the jQuery version numbers present in the 'jquery_releases.csv' file
version_numbers = get_version_numbers()

# create a JQueryVersion object for every version number
jQuery_versions = [JQueryVersion(element) for element in version_numbers]

# get the number of lines of code of these jQuery versions
get_lines_of_code(jQuery_versions)

# compute the relative size of each jQuery version
compute_relative_sizes(jQuery_versions)

# compute the heatmap's data, i.e. the coverage values for every pair of jQuery versions
heatmap_cells = compute_heatmap_data(jQuery_versions)

# transform the heatmap's data into a pandas DataFrame
dataframe = transform_into_dataframe(version_numbers, heatmap_cells)

# generate the heatmap corresponding to the dataframe
plot_heatmap(dataframe)
