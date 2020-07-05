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

separators = "{}[],="


def syntax_error(buf, message, *args):
    raise SyntaxError(str(buf), message.format(*args) if args else message)


def next_token(buf):
    token = ""
    while not buf.eof():
        ch = buf.next()
        if ch in separators:
            if token:
                if ch != ",":
                    buf.backup()
            else:
                token = ch
            break
        token += ch
    return token or None


def parse_valuelist(buf):
    """Parse a list of values."""
    result = []
    while True:
        t = next_token(buf)
        if t is None:
            syntax_error(str(buf), "value list misses closing ']'")
        if t == "]":
            return result
        if t == "[":
            result.append(parse_valuelist(buf))
            continue
        if t == "{":
            result.append(parse_kvpairs(buf))
            continue
        if t in "=}":
            syntax_error(buf, "unexpected in {} value list", repr(t))
        if t in ",":
            result.append("")
        result.append(t)


def parse_kvpairs(buf, need_brace=False):
    """Parse a kvpairs list `key=value,...`."""
    result = {}
    while True:
        # read key
        t = next_token(buf)
        if t is None:
            if need_brace:
                syntax_error(str(buf), "kvpairs list misses closing '}'")
            return result
        if t == "}":
            if not need_brace:
                syntax_error(str(buf), "unexpected '}' in top-level kvpairs")
            return result
        if t == ",":
            continue
        if t in separators:
            syntax_error(str(buf), "unexpected '{}' in kvpairs list", t)
        key = t
        # expect "="
        t = next_token(buf)
        if t != "=":
            syntax_error(str(buf), "expected '=' after key in kvpairs list")
        # read value
        t = next_token(buf)
        if t == "{":
            result[key] = parse_kvpairs(buf, need_brace=True)
            continue
        if t == "[":
            result[key] = parse_valuelist(buf)
            continue
        if t is ",":
            result[key] = ""
            continue
        # if t is "}":
        #     result[key] = ""
        #     return result
        if t is None:
            if need_brace:
                syntax_error(str(buf), "kvpairs list misses closing '}'")
            result[key] = ""
            return result
        result[key] = t


def parse_kvs(string):
    """Parse a key=value string and return the data structure."""
    return parse_kvpairs(StringReader(string))
