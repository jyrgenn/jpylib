# parser for key=value strings

"""Parser for key-value strings like "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f]}.

The data is returned as a Python data structure composed of strings,
dictionaries, and lists. It is used to set configuration values from
command-line arguments with a syntax more compact than e.g. JSON.

Syntax:

 * On the top level, the key-value string is a kvpairs list.

 * A kvpairs list is a list of zero or more key=value pairs separated by commas.
   It is mapped to a Python dictionary. Example:
   "signals=[1,2,15],action=terminate"

 * A key is a string that does not contain curly brackes, brackets, a comma, or
   an equals sign. Leading whitespace is not considered part of the key;
   trailing or embedded whitespace is a syntax error. For configuration values,
   it is helpful to match the syntax of Python identifiers, i.e. first character
   an underscore or a letter, following characters, if any, underscore, letter,
   or digit. These are mapped to Python dictionary keys. Example: "key_file"

 * A value can be a literal, a dictionary, or a list of values.

 * A literal value is a string of characters that doesn't contain curly brackes,
   brackets, a comma, or an equals sign. Whitespace is considered part of the
   literal. These are mapped to Python strings. Example: "Radio Dos"

 * A dictionary is a kvpairs list enclosed by curly braces. Example:
   "{file=~/etc/foo.conf,syntax=INI}"

 * A list is a list of zero or more values separated by commas and enclosed in
   brackets. Example: "[HUP,INTR,TERM]"

This syntax is obviously limited, but sufficient to express complex data
structures with (some) string values as leaves. It is mainly meant to be compact
for use on the command line.

The parser is somewhat sloppy and will accept some deviations from this
descriptsion, but exploiting this sloppyness will not be of any use.

"""

from .stringreader import StringReader

class SyntaxError(Exception):
    """An exception raised when the parser sees a syntax error.

    Its string argument is a string representation of the underlying
    StringReader with a marker behind the letter where the error was seen.

    """
    pass

def parse_value(buf):
    """Parse a value, which may be a literal, an assiciate array, or a list."""
    result = ""
    while not buf.eof():
        ch = buf.pop()
        if not result and ch == "[":
            return parse_list(buf)
        if not result and ch == "{":
            return parse_params(buf)
        if ch in "={[":
            raise SyntaxError(str(buf))
        if ch in ",]}":
            return result
        result += ch
    return result


def parse_list(buf):
    """Parse a list of values."""
    result = []
    while not buf.eof():
        result.append(parse_value(buf))
    return result


def parse_key(buf):
    """Terminated by `=`."""
    key = ""
    while not buf.eof():
        ch = buf.pop()
        if not key and ch.isspace():
            continue
        if ch == "=":
            return key
        if ch in " []{},":
            raise SyntaxError(str(buf))
        key += ch
    return key


def parse_kvpairs(buf):
    """Parse a parameter list `key=value,...`."""
    result = {}
    while not buf.eof():
        key = parse_key(buf)
        if not key:
            break
        result[key] = parse_value(buf)
    return result


def parse_kvs(string):
    """Parse a key=value string and return the data structure."""
    return parse_kvpairs(stringreader.StringReader(string))
