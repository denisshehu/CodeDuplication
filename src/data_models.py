class HeatmapCell:
    """
    This class represent a single cell on the heatmap.

    ...

    Attributes
    ----------

    row_version: JQueryVersion
        the jQuery version corresponding to the row of this cell

    column_version: JQueryVersion
        the jQuery version corresponding to the column of this cell

    clones_lines_of_code: int
        the total duplicate lines of code between the two jQuery versions of this cell

    coverage: float
        the coverage (i.e. similarity value) between the two jQuery versions of this cell

    Methods
    -------

    compute_coverage()
        computes the coverage that will be displayed on this cell
    """

    def __init__(self, row_version, column_version):
        """
        This is the constructor method of the class.

        :param row_version: the jQuery version corresponding to the cell's row
        :param column_version: the jQuery version corresponding to the cell's column
        """

        self.row_version = row_version
        self.column_version = column_version
        self.clones_lines_of_code = 0
        self.coverage = 0

    """ Getters and setters """

    def get_row_version(self):
        return self.row_version

    def get_column_version(self):
        return self.column_version

    def get_clones_lines_of_code(self):
        return self.clones_lines_of_code

    def get_coverage(self):
        return self.coverage

    def set_clones_lines_of_code(self, clones_lines_of_code):
        self.clones_lines_of_code = clones_lines_of_code
        pass

    def set_coverage(self, coverage):
        self.coverage = coverage
        pass

    def compute_coverage(self):
        """
        This method computes the coverage (i.e. similarity value) between the two jQuery versions of this cell.
        """

        coverage = self.clones_lines_of_code / (self.get_row_version().get_lines_of_code() +
                                                self.get_column_version().get_lines_of_code())
        self.set_coverage(coverage)
        pass


class JQueryVersion:
    """
    This class represents a version of jQuery.

    ...

    Attributes
    ----------

    version_number: str
        the jQuery's version number

    lines_of_code: int
        the total number of lines of code (including comments and blank lines) of the jQuery's version

    relative_size: float
        the relative size of the jQuery's version
    """

    def __init__(self, version_number):
        """
        This is the constructor method of the class.

        :param version_number: the jQuery's version number
        """

        self.version_number = version_number
        self.lines_of_code = 0
        self.relative_size = 0

    """ Getters and setter """

    def get_version_number(self):
        return self.version_number

    def get_lines_of_code(self):
        return self.lines_of_code

    def set_lines_of_code(self, lines_of_code):
        self.lines_of_code = lines_of_code

    def get_relative_size(self):
        return self.relative_size

    def set_relative_size(self, relative_size):
        self.relative_size = relative_size


class JsInspectInstance:
    """
    This class represents an instance from the reported result of 'jsinspect',
    i.e. it represents a portion of code that is a duplicate between two jQuery versions.

    ...

    Attributes
    ----------

    path: str
        the file's path where the duplicated code is

    starting_index: int
        the line of code where the duplicated code starts

    ending_index: int
        the line of code where the duplicated code ends
    """

    def __init__(self, path, starting_index, ending_index):
        """
        This is the constructor method of the class.

        :param path: the file's path
        :param starting_index: the starting index of the duplicated code
        :param ending_index: the ending index of the duplicated code
        """

        self.path = path
        self.starting_index = starting_index
        self.ending_index = ending_index

    """ Getters and setters """

    def get_path(self):
        return self.path

    def get_starting_index(self):
        return self.starting_index

    def get_ending_index(self):
        return self.ending_index
