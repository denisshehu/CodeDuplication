# CodeDuplication

## Introduction

This repository is the implementation part of the second assignment of the course _Software Evolution_
at the Eindhoven University of Technology (https://www.tue.nl/en/).

The aim of the project was to investigate the evolution of jQuery's source code by analyzing 83 official
versions of it. (https://github.com/jquery/jquery)

After execution, this tool generates a heatmap where each cell represents the similarity between the two jQuery versions
corresponding to its row and column.

## Implementation

The tool's flow is the following:
* Firstly, all the jQuery versions are downloaded.
* Then, the number of lines of the source code for every jQuery version is computed using `cloc`
  (https://github.com/AlDanial/cloc).
* Next, `jsinspect` (https://github.com/danielstjules/jsinspect) is used to report the duplicate lines of code between every pair of jQuery versions.
* The results reported by `jsinspect` need processing before they can be used, e.g.: some lines of duplicate code
  might be reported more than once and different duplicate portions might overlap. After this processing,
  the total number of duplicated code for each pair of jQuery versions is known.
* The coverage (i.e. similarity value) for every pair of jQuery versions is computed as the ratio between the number of lines of duplicated code and the sum of total lines of code of these versions.
* A `pandas.DataFrame` is created storing these coverage values.
* The heatmap corresponding to the dataframe is generated and stored as a .png file.

### Other

The resulting heatmap can be found in this repository in the **src** directory.

This tool runs inside of Docker.