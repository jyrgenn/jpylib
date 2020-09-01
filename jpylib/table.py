# table generator

import jpylib as y
import functools


class Table:

    def __init__(self, *, corner=["", "", "", ""], border=["", "", "", ""],
                 hsep=["", ""], vsep=["", ""], tb_cross=["", ""],
                 lb_cross=["", ""], rb_cross=["", ""], bb_cross=["", ""],
                 hl_cross=["", ""], nl_cross=["", ""], cell_pad=[" ", " "],
                 pad_char=" ", template=None, align=None, data=None):
        """Initialise a Table formatting parameter set.
        
        Arguments:
        * corner[4]:   top left, top right, bottom left, bottom right corners
        * border[4]:   top, left, right, bottom border sans crossing or corner
        * hsep[2]:     horizontal separator, after first column and others
        * vsep[2]:     vertical separator, after first row and others
        * tb_cross[2]: top border crossing, first and others
        * lb_cross[2]: left border crossing, first and others
        * rb_cross[2]: right border crossing, first and others
        * bb_cross[2]: bottom border crossing, first and others
        * hl_cross[2]: header separator line crossing, first and others
        * nl_cross[2]: normal separator line crossing, first and others
        * cell_pad[2]: minimum cell padding, left and right
        * pad_char:    padding character
        * template:    a template 7 x 7 drawing describing the table
        * align:       alignment descriptor string, 1 char per column, l/r/c;
                       may be sequence of 2 for first and following rows;
                       asterisk at the end means default for folloing columns
                       is the character in front of the asterisk
        """
        self.__dict__.update(locals())
        if template:
            self._from_template(template)

        if cell_pad is None:
            self.cell_pad = ["", ""]
        elif y.is_sequence(cell_pad):
            if len(cell_pad) == 1:
                self.cell_pad = cell_pad * 2
            else:
                self.cell_pad = cell_pad[:2]
        elif isinstance(cell_pad, str):
            self.cell_pad = [cell_pad, cell_pad]
        else:
            ValueError("cell_pad is not None or str or sequence of 2: {}"
                       .format(repr(cell_pad)))

        # Always have a separate alignment for the first and the following
        # lines. They need not be different, though.
        self.defaultalign = [None, None]
        if align is None:
            self.align = ["", ""]
        elif type(align) == str:
            self.align = [align, align]
        else:
            try:
                if len(align) == 1:
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
        if data:
            self._fill(data)

    def _from_template(self, template):
        def s(char):
            return "" if char == "0" else char

        tl = [l.strip() for l in template.strip().split("\n")]
        assert len(tl) == 7, \
            "template must have 7 lines, not {}".format(len(tl))
        for i, l in enumerate(tl):
            assert len(l) == 7, \
                "template line must b 7 chars long, not {} (line {})".format(
                    len(l), i)
        self.corner = [s(tl[0][0]), s(tl[0][6]), s(tl[6][0]), s(tl[6][6])]
        self.border = [s(tl[0][1]), s(tl[1][0]), s(tl[1][6]), s(tl[6][1])]
        self.hsep = [s(tl[1][2]), s(tl[1][4])]
        self.vsep = [s(tl[2][1]), s(tl[4][1])]
        self.tb_cross = [s(tl[0][2]), s(tl[0][4])]
        self.lb_cross = [s(tl[2][0]), s(tl[4][0])]
        self.rb_cross = [s(tl[2][6]), s(tl[4][6])]
        self.bb_cross = [s(tl[6][2]), s(tl[6][4])]
        self.hl_cross = [s(tl[2][2]), s(tl[2][4])]
        self.nl_cross = [s(tl[4][2]), s(tl[4][4])]
        

    def _fill(self, data):
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
        return (self.pad_char * lpad
                + self.cell_pad[0]
                + str(item)
                + self.cell_pad[1]
                + self.pad_char * rpad)

    def _vert_sep(self, left_border, right_border, line, cross1, cross2):
        r = []
        if line:
            r.append(left_border)
            had_first_col = False
            cross = cross1
            for col in range(self.cols):
                if had_first_col:
                    r.append(cross)
                    cross = cross2
                had_first_col = True
                r.append(line * (self.col_width[col] + len(self.cell_pad[0]
                                                           + self.cell_pad[1])))
            r.append(right_border)
        result = "".join(r)
        if result:
            return result + "\n"
        return ""
            

    def _alignment(self, row, column):
        index = 0 if row == 0 else 1
        align = self.align[index]
        if column >= len(align or ""):
            return self.defaultalign[index]
        return align[column]


    def format(self, data=None):
        """Return the formatted Table as a string. Data must be present."""

        if data:
            self._fill(data)
        assert self.data, "Table has no data yet, so cannot be formatted."
        r = [self._vert_sep(self.corner[0], self.corner[1],
                            self.border[0], self.tb_cross[0], self.tb_cross[1])]
        had_first_row = False
        left_cross, int_cross1, int_cross2, right_cross = (
            self.lb_cross[0], self.hl_cross[0],
            self.hl_cross[1], self.rb_cross[0]
        )
        vsep = self.vsep[0]
        for row, data_line in enumerate(self.data):
            if had_first_row:
                r.append(self._vert_sep(left_cross, right_cross,
                                        vsep, int_cross1, int_cross2))
                left_cross, int_cross1, int_cross2, right_cross = (
                    self.lb_cross[1], self.nl_cross[0],
                    self.nl_cross[1], self.rb_cross[1]
                )
                vsep = self.vsep[1]
            had_first_row = True

            had_first_col = False
            hsep = self.hsep[0]
            r.append(self.border[1])
            for col, data_item in enumerate(data_line):
                if had_first_col:
                    r.append(hsep)
                    hsep = self.hsep[1]
                had_first_col = True
                r.append(self._pad(str(data_item), self.col_width[col],
                                   self._alignment(row, col)))
            r.append(self.border[2])
            r.append("\n")
                
        # bottom border
        r.extend(self._vert_sep(self.corner[2], self.corner[3],
                                self.border[3], *self.bb_cross))
        return "".join(r)