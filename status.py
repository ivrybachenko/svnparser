"""
Script that transforms 'svn status -uv' output into readable table form
"""
import sys
import argparse


class ParseException(Exception):
    pass


class Column:
    """
    Abstract column
    """
    alignment = '^'
    width = 0
    title = 'Unnamed'
    _transformation_map = {}

    def __init__(self, width=0, title='Unnamed', alignment='^'):
        """
        :param width: Column width
        :param title: Column title
        :param alignment: Column alignment. Possible values: '^' - center, '<' - left, '>' - right
        """
        if alignment in ['<', '^', '>']:
            self.__alignment = alignment
        else:
            self.__alignment = '^'

        self.title = title

        if width <= 0:
            self.width = len(self.title)
        else:
            self.width = width

    def build_value(self, line_to_parse):
        """
        Retrieves the value from line amd transforms it into readable form.
        Can raise a ParseException if value can't be retrieved
        """
        value = self._retrieve_value(line_to_parse)
        return self._transform_value(value)

    def fit_to_width(self, value):
        """
        Crops value to column width. Applies alignment.
        """
        pattern = '{{:{a}{w}.{w}s}}'.format(a=self.__alignment, w=self.width)
        return pattern.format(value)

    def _transform_value(self, value):
        """
        Transforms value into readable form
        """
        if value not in self._transformation_map.keys():
            return value
        return self._transformation_map[value]

    def _retrieve_value(self, line_to_parse):
        """
        Retrieves the value of corresponding column from line
        Can raise a ParseException if value can't be retrieved
        """
        pass


class StatusColumn(Column):
    """
    This column indicates that an item was added, deleted, or otherwise changed
    """
    _transformation_map = {
        ' ': ' ',  # No modifications.

        'M': 'Modified',  # Item has been modified.

        'D': 'Deleted',  # Item is scheduled for deletion.

        'A': 'Added',  # Item is scheduled for addition.

        'R': 'Replaced',  # Item has been replaced in your working copy.
        #  This means the file was scheduled for deletion, and then a new file
        #  with the same name was scheduled for addition in its place.

        'C': 'Conflicts',  # The contents (as opposed to the properties) of the item
        #  conflict with updates received from the repository.

        'X': 'External',  # Item is present because of an externals definition.

        'I': 'Ignored',  # Item is being ignored (e.g., with the svn:ignore property).

        '?': 'Not controlled',  # Item is not under version control.

        '!': 'Missed',  # Item is missing (e.g., you moved or deleted it without using svn).
        #  This also indicates that a directory is incomplete (a checkout or update was interrupted).

        '~': 'Kind replaced'  # Item is versioned as one kind of object (file, directory, link),
        #  but has been replaced by a different kind of object.
    }

    def __init__(self, width=0, title='Status', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        if len(line_to_parse) <= 0:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[0]
        return value

    def is_controlled(self, line_to_parse):
        """
        Parse line and checks whether the item is controlled by Version Control System
        Can raise a ParseException if value can't be retrieved
        :return: True if item is controlled. Else False.
        """
        return self._retrieve_value(line_to_parse) not in ['?', 'I']


class PropertiesColumn(Column):
    """
    This column tells the status of a file's or directory's properties
    """
    _transformation_map = {
        ' ': ' ',  # No modifications.

        'M': 'Modified',  # Properties for this item have been modified.

        'C': 'Conflict'  # Properties for this item are in conflict with property updates received from the repository.
    }

    def __init__(self, width=0, title='Props', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'Properties' column is the symbol on the 2nd position
        if len(line_to_parse) <= 1:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[1]
        return value


class IsLockedColumn(Column):
    """
    This column is populated only if the working copy directory is locked
    """
    _transformation_map = {
        ' ': ' ',  # Item is not locked.

        'L': 'Locked'  # Item is locked.
    }

    def __init__(self, width=0, title='isLocked', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'IsLocked' column is the symbol on the 3rd position
        if len(line_to_parse) <= 2:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[2]
        return value


class AddWithHistColumn(Column):
    """
    This column is populated only if the item is scheduled for addition-with-history
    """
    _transformation_map = {
        ' ': ' ',  # No history scheduled with commit.

        '+': '+'  # History scheduled with commit.
    }

    def __init__(self, width=0, title='AddWithHist', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'AddWithHist' column is the symbol on the 4th position
        if len(line_to_parse) <= 3:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[3]
        return value


class SwitchedToParentColumn(Column):
    """
    This column is populated only if the item is switched relative to its parent
    """
    _transformation_map = {
        ' ': ' ',  # Item is a child of its parent directory.

        'S': 'Switched'  # Item is switched.
    }

    def __init__(self, width=0, title='SwitchedToParent', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'AddWithHist' column is the symbol on the 5th position
        if len(line_to_parse) <= 4:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[4]
        return value


class LockInfoColumn(Column):
    """
    This column is populated with lock information
    """
    _transformation_map = {
        ' ': ' ',  # When --show-updates (-u) is used, the file is not locked.
        #  If --show-updates (-u) is not used, this merely means
        # that the file is not locked in this working copy.

        'K': 'Token',  # File is locked in repository, lock toKen present

        'O': 'Other',  # File is locked either by another user or in another working copy.
        #  This appears only when --show-updates (-u) is used.

        'T': 'Stolen',  # File was locked in this working copy, but the lock has been “stolen” and is invalid.
        #  The file is currently locked in the repository.
        #  This appears only when --show-updates (-u) is used.

        'B': 'Broken'  # File was locked in this working copy, but the lock has been “broken” and is invalid.
        #  The file is no longer locked. This appears only when --show-updates (-u) is used.
    }

    def __init__(self, width=0, title='LockInfo', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'LockInfo' column is the symbol on the 6th position
        if len(line_to_parse) <= 5:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[5]
        return value


class ConflictColumn(Column):
    """
    This column is populated only if the item is the victim of a tree conflict
    """
    _transformation_map = {
        ' ': ' ',  # Item is not the victim of a tree conflict.

        'C': 'Conflict'  # Item is the victim of a tree conflict.
    }

    def __init__(self, width=0, title='Conflict', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'Conflict' column is the symbol on the 7th position
        if len(line_to_parse) <= 6:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[6]
        return value

    def is_conflict_description(self, line_to_parse):
        """
        Checks whether the line represents a conflict description
        Can raise a ParseException if value can't be retrieved
        """
        if len(line_to_parse) <= 6:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        return line_to_parse[6] == '>'


class OutOfDateColumn(Column):
    """
    This column shows whether a newer revision of the item exists on the server
    """
    _transformation_map = {
        ' ': ' ',  # The item in your working copy is up to date.

        '*': 'Out of date'  # A newer revision of the item exists on the server.
    }

    def __init__(self, width=0, title='Out of date', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'OutOfDate' column is the symbol on the 9th position
        if len(line_to_parse) <= 8:
            raise ParseException("Can not parse column '{col}'. Line is too short".format(col=self.title))
        value = line_to_parse[8]
        return value


class WorkingRevisionColumn(Column):
    """
    This column shows a working revision
    """

    def __init__(self, width=0, title='Working revision', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'Working revision' column is the 1st word after 'OutOfDate' column
        tail = line_to_parse[10:].split()
        if len(tail) < 0:
            raise ParseException(
                "Can not parse column '{col}'.".format(col=self.title))
        value = tail[0]
        return value


class CommittedRevisionColumn(Column):
    """
        This column shows the last committed revision
    """

    def __init__(self, width=0, title='Committed revision', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'Committed revision' column is the 2nd word after 'OutOfDate' column
        tail = line_to_parse[10:].split()
        if len(tail) < 2:
            raise ParseException(
                "Can not parse column '{col}'.".format(col=self.title))
        value = tail[1]
        return value


class CommittedAuthorColumn(Column):
    """
    This column shows the last committed author
    """

    def __init__(self, width=0, title='Committed author', alignment='^'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then column is empty
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return ''
        # 2 case) 'Committed revision' column is the 3rd word after 'OutOfDate' column
        tail = line_to_parse[10:].split()
        if len(tail) < 3:
            raise ParseException(
                "Can not parse column '{col}'.".format(col=self.title))
        value = tail[2]
        return value


class WorkingCopyPathColumn(Column):
    """
    This column shows a working copy path
    """

    def __init__(self, width=50, title='Working copy path', alignment='<'):
        super().__init__(width=width, title=title, alignment=alignment)

    def _retrieve_value(self, line_to_parse):
        # 1 case) if item is not under version control system
        #               then 'path' column is right after the 'status' column
        controlled = StatusColumn().is_controlled(line_to_parse)
        if not controlled:
            return line_to_parse[1:].strip()
        # 2 case) if --verbose flag was passed
        #               then 'path' column is right after the 'last committed author' column
        author = CommittedAuthorColumn().build_value(line_to_parse)
        start_of_last_column = line_to_parse.find(author) + len(author)
        value = line_to_parse[start_of_last_column:].strip()
        if value == '':
            raise ParseException("Can not parse column '{col}'.".format(col=self.title))
        return value


class Table:
    """
    Table
    """
    left_separator = ' '
    right_separator = ' '
    column_separator = ' | '
    header_separator = '='
    row_separator = '-'

    columns = []
    cols_count = 0
    table_width = 0  # width of table (including column separators)

    def __init__(self, columns, column_separator=' | ', left_separator=' ',
                 right_separator=' ', header_separator='=', row_separator='-'):
        """
        :param columns: Table columns. Must be a list with elements of 'Column' class
        :param left_separator: String printed in the left of table
        :param column_separator: String that separates 2 columns
        :param right_separator: String printed in the right of table
        :param header_separator: Character that separates header and body
        :param row_separator: Character that separates 2 rows
        """
        self.left_separator = left_separator
        self.right_separator = right_separator
        self.column_separator = column_separator
        self.header_separator = header_separator
        self.row_separator = row_separator

        self.columns = columns
        self.cols_count = len(self.columns)

        sep_count = self.cols_count - 1
        total_sep_width = len(self.left_separator) + len(self.right_separator) + sep_count * len(self.column_separator)
        self.table_width = total_sep_width
        for col in self.columns:
            self.table_width += col.width

    def build_header(self):
        """
        Builds a header. Column names a wrapped to width.
        :return: String representing a header
        """
        row = []
        for col in self.columns:
            value = col.title
            row.append(value)
        row = self.__wrap_row(row)
        row = self.__join_row(row)
        return row

    def build_row(self, line_to_parse):
        """
        Parse line, transforms values and wraps them to width if necessary.
        :return: String representing a row
        """
        if ConflictColumn().is_conflict_description(line_to_parse):
            row = line_to_parse[:-1]
        else:
            row = self.__parse_transform_line(line_to_parse)
            row = self.__wrap_row(row)
            row = self.__join_row(row)
        return row

    def build_row_separator(self):
        """
        Returns the line which is used to separate two rows
        """
        return self.row_separator * self.table_width

    def build_header_separator(self):
        """
        Prints the line which is used to separate header and row
        """
        return self.header_separator * self.table_width

    def __join_row(self, multiline_row):
        """
        Transforms multiline row to String
        :param multiline_row: 2-dimensional list of strings. 1st dimension states for the rows, 2nd - for the columns.
        :return: String
        For example:
        Input:
        [
            ['col1', 'col2'], # <- line1
            ['col1', 'col2']  # <- line2
        ]
        Output:
            'col1|col2'+'\n'+
            'col1|col2'
        """
        res = []
        for line in multiline_row:
            joined = self.column_separator.join(line)
            joined = self.left_separator + joined + self.right_separator
            res.append(joined)
        res = '\n'.join(res)
        return res

    def __parse_transform_line(self, line_to_parse):
        """
        Parse line into list of columns' values. Transforms it into a readable form.
        :return: List which elements can be treated as values of corresponding column
        """
        row = []
        for col in self.columns:
            value = col.build_value(line_to_parse)
            row.append(value)
        return row

    def __wrap_row(self, row):
        """
        Wraps row values to width.
        :param row: List of strings, e.g. ['cat','dog']
        :return: Returns a 2-dimensional list of strings. 1st dimension states for the rows, 2nd - for the columns.
        Input:
        ['column1', 'column2']
        Output:
        [
            [' colu ', ' colu '],  <- line1
            [' mn1  ', ' mn2  ']   <- line2
        ]
        """
        multiline_row = []
        while not self.__is_row_empty(row):
            line = []
            for i in range(self.cols_count):
                width = self.columns[i].width
                value = row[i][:width]
                value = self.columns[i].fit_to_width(value)
                row[i] = row[i][width:]
                line.append(value)
            multiline_row.append(line)
        return multiline_row

    @staticmethod
    def __is_row_empty(row):
        """
        Checks whether all elements of row are empty
        :param row: List of strings, e.g. ['cat','dog']
        """
        for val in row:
            if len(val) != 0:
                return False
        return True


class RowWriter:
    """
    Class for writing table rows to some output
    """

    def write(self, row):
        """
        Writes the row to an output
        """
        pass


class ConsoleRowWriter(RowWriter):
    """
    Class for writing table rows to console
    """

    def write(self, row):
        print(row)


class FileRowWriter(RowWriter):
    """
    Class for writing table rows to file
    """
    __file = None

    def __init__(self, file):
        """
        :param file: Output file
        """
        self.__file = file

    def write(self, row):
        self.__file.write(row + '\n')


class SVNStatusTransformApp:
    """
    Main class
    """
    args = None

    def __init__(self):
        parser = self.__create_parser()
        self.args = parser.parse_args(sys.argv[1:])

    def run(self):
        text_to_parse = self.args.input_file.readlines()
        row_writer = ConsoleRowWriter() if self.args.output is None \
            else FileRowWriter(self.args.output)
        table = self.__create_table()
        self.__print_table(table, text_to_parse, row_writer)

    def __create_parser(self):
        argument_parser = argparse.ArgumentParser(description='''Script that transforms 'svn status -uv' 
                                                                  output into readable table form''')
        argument_parser.add_argument('input_file', type=argparse.FileType(),
                                     help="File with output of 'svn status -uv' command ")
        argument_parser.add_argument('-o', '--output', type=argparse.FileType(mode='w'),
                                     help='File to write script output')
        argument_parser.add_argument('-w', '--width', type=int, nargs=2, action='append',
                                     metavar=('INDEX', 'WIDTH'), default=[],
                                     help='Set column width. Column index is 0-based')

        return argument_parser

    def __create_table(self):
        columns = [
            StatusColumn(),
            PropertiesColumn(),
            IsLockedColumn(),
            AddWithHistColumn(),
            SwitchedToParentColumn(),
            LockInfoColumn(),
            ConflictColumn(),
            OutOfDateColumn(),
            WorkingRevisionColumn(),
            CommittedRevisionColumn(),
            CommittedAuthorColumn(),
            WorkingCopyPathColumn()
        ]
        col_cnt = len(columns)
        for [i, w] in self.args.width:
            if 0 <= i < col_cnt:
                columns[i].width = w
        table = Table(columns, left_separator='| ', right_separator=' |')
        return table

    def __print_table(self, table, lines_to_parse, row_writer):
        """
        Parse lines and prints them using specified row_writer
        :param lines_to_parse: 'svn status -uv' output
        :param row_writer: Element of class 'RowWriter'
        """
        header_sep = table.build_header_separator()
        row_sep = table.build_row_separator()

        header = table.build_header()
        row_writer.write(header)
        row_writer.write(header_sep)

        for line in lines_to_parse:
            try:
                row = table.build_row(line)
            except ParseException as e:
                print('!' * table.table_width)
                print('Error while parsing line. Line:')
                print(line)
                print(e)
                print('!' * table.table_width)
                sys.exit()
            row_writer.write(row)
            row_writer.write(row_sep)


if __name__ == '__main__':
    app = SVNStatusTransformApp()
    app.run()
