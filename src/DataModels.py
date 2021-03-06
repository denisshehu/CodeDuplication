class HeatmapCell:

    def __init__(self, row_version, column_version):
        self.rowVersion = row_version
        self.columnVersion = column_version


class JQueryVersion:

    def __init__(self, version_number):
        self.version_number = version_number
        self.lines_of_code = 0

    def add_lines_of_code(self, lines_of_code):
        self.lines_of_code = lines_of_code
