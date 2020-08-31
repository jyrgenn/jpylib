# table generator

import jpylib as y
import functools

class Table:

    def __init__(self, *, data=None, have_header=False, align=None,
                 vsep="-", hsep="|", Hsep="=", header_cross="=",
                 field_pad=1, field_vpad=0, pad_char=" ",
                 side_border="|", tb_border="-",
                 int_cross="+", side_cross="|", tb_cross="-", corner="+"):
        """Initialise a Table object. Parameters:
        * data:        a sequence of rows, which are sequences of data items
        * have_header: if true, first row in data is a header row
        * align:       alignment descriptor string, 1 char per column, l/r/c;
                       may be sequence of 2 for first and following rows;
                       asterisk at the end means default for folloing columns
                       is the character in front of the asterisk
        * vsep:        vertical separator (no separator line if None),
                       or a sequence of 2 for first and following separators
        * hsep:        horizontal separator
        * field_pad:   minimum horizontal padding of a field on both sides
        * field_vpad:  vertical padding of the items in a cell
        * pad_char:    padding character
        * side_border: border on the side of the table
        * tb_border:   border on the top and bottom of the table
        * int_cross:   internal crossing point
        * side_cross:  crossing point on the side of the table
        * tb_cross:    crossing point at top or bottom of the table
        * corner:      table corner

        """
        self.__dict__.update(locals())
        # Always have a separate alignment for the first and the following
        # lines. They need not be different, though.
        self.defaultalign = [None, None]
        if align is None:
            self.align = ["", ""]
        elif type(align) == str:
            self.align = [align, align]
        else:
            try:
                if len(align) < 1:
                    self.align = [align[0], align[0]]
            except:
                ValueError("align must be string or a sequence of strings, "
                           + "but is {}".format(repr(align)))
        # Set default alignment if align ends with "*"
        for i in (0, 1):
            if self.align[i]:
                if self.align[i].endswith("*") and len(self.align[i]) > 1:
                    self.defaultalign[i] = self.align[i][-2]
                    self.align[i] = self.align[i][:-1]
        print("self.defaultalign", self.defaultalign)
        if data:
            self.content(data, have_header)

    def content(self, data, have_header=False):
        """Assess and store the table data."""
        self.data = data
        self.have_header = have_header
        self.cols = 0                   # maximum column number
        self.rows = 0                   # maximum row number
        self.col_width = []             # maximum item width per columns

        for row, data_line in enumerate(data):
            self.rows = row + 1
            for col, data_item in enumerate(data_line):
                col_width = self.col_width
                if col >= self.cols:
                    self.cols = col + 1
                    self.col_width.append(0)
                self.col_width[col] = \
                    max(self.col_width[col], len(str(data_item)))
        return self                     # so we can do Table().from().string()

    def _pad(self, item, width, alignment, pad_char=None):
        """Return a list of the item with left and right padding."""
        padc = pad_char or self.pad_char
        padding = width - len(item)
        if alignment is None:
            if y.is_int(item):
                alignment = "r"
            else:
                alignment = "l"                
        if alignment == "l":
            lpad = 0
            rpad = padding
        elif alignment == "r":
            lpad = padding
            rpad = 0
        elif alignment == "c":
            lpad = int(padding / 2)
            rpad = padding - lpad
        else:
            raise ValueError("invalid char in alignment: {}"
                             .format(repr(alignment)))
        return [(padc * lpad), str(item), (padc * rpad)]

    def _vert_sep(self, border, line, cross):
        r = []
        r.append(border)
        had_first_col = False
        for col in range(self.cols):
            if had_first_col:
                r.append(cross)
            had_first_col = True
            r.append(line * (self.col_width[col] + 2))
        r.append(border)
        r.append("\n")
        return r
            

    def _alignment(self, row, column):
        index = 0 if row == 0 else 1
        align = self.align[index]
        if column >= len(align or ""):
            return self.defaultalign[index]
        return align[column]


    def format(self, data=None, have_header=False):
        """Return the formatted Table as a string. Data must be present."""

        if data:
            self.content(data, have_header)
        assert self.data, "Table has no data yet, so cannot be formatted."
        r = self._vert_sep(self.corner, self.tb_border, self.tb_cross)

        had_first_row = False
        header_sep = self.have_header
        padding = self.pad_char * self.field_pad
        for row, data_line in enumerate(self.data):
            if had_first_row:
                if header_sep:
                    vsep = self.Hsep
                    cross = self.header_cross
                else:
                    vsep = self.vsep
                    cross = self.int_cross
                header_sep = False
                r.extend(self._vert_sep(self.side_cross, vsep, cross))
            had_first_row = True

            r.append(self.side_border)
            r.append(padding)
            had_first_col = False
            for col, data_item in enumerate(data_line):
                if had_first_col:
                    r.append(padding)
                    r.append(self.hsep)
                    r.append(padding)
                had_first_col = True
                r.extend(self._pad(str(data_item), self.col_width[col],
                                  self._alignment(row, col)))
            r.append(self.pad_char)
            r.append(self.side_border)
            r.append("\n")
                
        # bottom border
        r.extend(self._vert_sep(self.corner, self.tb_border, self.tb_cross))

        return "".join(r)
