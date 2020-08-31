# table generator

import jpylib as y
import functools

def _prepare_sep(name, sep):
    """Always return a seqence of two."""
    if sep is None:
        return [None, None]
    if type(sep) == str:
        if len(sep) == 1:
            return [sep[0], sep[0]]
        if len(sep) >= 2:
            return [sep[0], sep[1]]
    elif y.is_sequence(sep):
        if len(sep) == 0:
            return [None, None]
        elif len(sep) == 1:
            return [sep[0], sep[0]]
        else:
            return [sep[0], sep[1]]
    ValueError("{} must be list or string of length 1 or 2, but is {}"
               .format(name, repr(sep)))

class Table:

    def __init__(self, *, data=None, align=None, vsep="-", hsep="|",
                 cell_pad=1, pad_char=" ", border="-||-", cross="-|-||-|-",
                 corner="+"):
        """Initialise a Table object. Parameters:
        * data:        a sequence of rows, which are sequences of data items
        * align:       alignment descriptor string, 1 char per column, l/r/c;
                       may be sequence of 2 for first and following rows;
                       asterisk at the end means default for folloing columns
                       is the character in front of the asterisk
        * vsep:        vertical separator (no separator line if None),
                       may be two characters for first and following vseps
        * hsep:        horizontal separator, may be two characters for first
                       and following hseps
        * cell_pad:    minimum number of horizontal padding chars in a cell
                       on both sides (may be array of two values)
        * pad_char:    cell padding character
        * border:      table border, string of 4 (top, left, right, bottom)
        * cross:       string of 1 or 8 (top, header left, header intern,
                       header right, left, intern, right, bottom)
        * corner:      table corner, string of 1 or 4 (top left, top right,
                       bottom left, bottom right)

        """
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
                else:
                    self.align = [align[0], align[1]]
            except:
                ValueError("align must be string or a sequence of strings, "
                           + "but is {}".format(repr(align)))
        # Set default alignment if align ends with "*"
        for i in (0, 1):
            if self.align[i]:
                if self.align[i].endswith("*") and len(self.align[i]) > 1:
                    self.defaultalign[i] = self.align[i][-2]
                    self.align[i] = self.align[i][:-1]
        # Always have arrays of two vseps and two hseps
        self.vsep = _prepare_sep("vsep", vsep)
        self.hsep = _prepare_sep("hsep", hsep)

        # Always have two cell_pads (left and right) and the pad_char
        if isinstance(cell_pad, int):
            self.cell_pad = (pad_char * cell_pad, pad_char * cell_pad)
        elif y.is_sequence(cell_pad) and len(cell_pad) == 2:
            self.cell_pad = (pad_char * cell_pad[0], pad_char * cell_pad[1])
        else:
            ValueError("cell_pad must be int or sequence of 2 ints, but is "
                       + repr(cell_pad))
        self.pad_char = pad_char

        # Have a border of 4
        if border is None:
            self.border = [""] * 4
        elif type(border) is str and len(border) == 4:
            self.border = list(border)
        else:
            ValueError("border must be a string of 4, but is " + repr(border))

        # Always have a list of four corners
        if type(corner) is str and len(corner) == 1:
            self.corner = list(corner * 4)
        elif type(corner) is str and len(corner) == 4:
            self.corner = list(corner)
        else:
            ValueError("corner must be a string of length 1 or 4, but is "
                       + repr(corner))
        # Always have a list of six crosses
        if type(cross) is str and len(cross) == 1:
            self.cross = list(cross * 8)
        elif type(cross) is str and len(cross) == 8:
            self.cross = list(cross)
        else:
            ValueError("cross must be a string of length 1 or 6, but is "
                       + repr(cross))
        if data:
            self.content(data)

    def content(self, data):
        """Assess and store the table data."""
        self.data = data
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

    def _pad(self, item, width, alignment):
        """Return a list of the item with left and right padding."""
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
        return [(self.pad_char * lpad), str(item), (self.pad_char * rpad)]

    def _vert_sep(self, left_border, right_border, line, cross):
        r = []
        if line:
            r.append(left_border)
            had_first_col = False
            for col in range(self.cols):
                if had_first_col:
                    r.append(cross)
                had_first_col = True
                r.append(line * (self.col_width[col] + 2))
            r.append(right_border)
            r.append("\n")
        return r
            

    def _alignment(self, row, column):
        index = 0 if row == 0 else 1
        align = self.align[index]
        if column >= len(align or ""):
            return self.defaultalign[index]
        return align[column]


    def format(self, data=None):
        """Return the formatted Table as a string. Data must be present."""

        if data:
            self.content(data)
        assert self.data, "Table has no data yet, so cannot be formatted."
        r = self._vert_sep(self.corner[0], self.corner[1],
                           self.border[0], self.cross[0])

        had_first_row = False
        left_cross, int_cross, right_cross = self.cross[1:4]
        vsep = self.vsep[0]
        for row, data_line in enumerate(self.data):
            if had_first_row:
                r.extend(self._vert_sep(left_cross, right_cross,
                                        vsep, int_cross))
                left_cross, int_cross, right_cross = self.cross[4:7]
                vsep = self.vsep[1]
            had_first_row = True

            if self.border[1]:
                r.append(self.border[1])
                r.append(self.cell_pad[0])
            had_first_col = False
            hsep = self.hsep[0]
            for col, data_item in enumerate(data_line):
                if had_first_col:
                    r.append(self.cell_pad[1])
                    if hsep:
                        r.append(hsep)
                    r.append(self.cell_pad[0])
                    hsep = self.hsep[1]
                had_first_col = True
                r.extend(self._pad(str(data_item), self.col_width[col],
                                  self._alignment(row, col)))
            if self.border[2]:
                r.append(self.cell_pad[1])
                r.append(self.border[2])
            r.append("\n")
                
        # bottom border
        r.extend(self._vert_sep(self.corner[2], self.corner[3],
                                self.border[3], self.cross[7]))
        return "".join(r)
