class HeatmapCell:

    def __init__(self, row_version, column_version):
        self.row_version = row_version
        self.column_version = column_version
        self.clones_lines_of_code = 0
        self.coverage = 0

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
        coverage = self.clones_lines_of_code / (self.get_row_version().get_lines_of_code() +
                                                self.get_column_version().get_lines_of_code())
        self.set_coverage(coverage)
        pass


class JQueryVersion:

    def __init__(self, version_number):
        self.version_number = version_number
        self.lines_of_code = 0

    def get_version_number(self):
        return self.version_number

    def get_lines_of_code(self):
        return self.lines_of_code

    def set_lines_of_code(self, lines_of_code):
        self.lines_of_code = lines_of_code


class JsInspectInstance:

    def __init__(self, path, starting_index, ending_index):
        self.path = path
        self.starting_index = starting_index
        self.ending_index = ending_index

    def get_path(self):
        return self.path

    def get_starting_index(self):
        return self.starting_index

    def get_ending_index(self):
        return self.ending_index
