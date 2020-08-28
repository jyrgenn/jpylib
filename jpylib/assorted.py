# assorted smallish functions

import collections

# Yes, this is a bit silly. But hey...
means_true = \
  set("yes y sure ja j jou si on oui t true  aye 1 affirmative".split())
means_false = \
  set("no n  nope nein nee   off non f false nay 0 negative".split())

def boolish(value, default=None):
    """Return a truth value for the argument.

    If that cannot be determined, fall back to default (if not None) or raise a
    ValueError exception. This can be used for parsing config files (that aren't
    Python) or interactive answers or the like.

    """

    val = value.strip().lower()
    if val in means_true:
        return True
    if val in means_false:
        return False
    if default is None:
        raise ValueError("value '{}' cannot be understood as false or true".
                         format(value))
    else:
        return default


def flatten(seq):
    """Flatten a nested sequence into a flat one with the same elements.

    Return a flat generator object containing just the elements. If the
    argument is a string or not a sequence, the generator object will
    contain just the argument.

    """
    if not isinstance(seq, str) and isinstance(seq, collections.abc.Iterable):
        for elem in seq:
            yield from flatten(elem)
    else:
        yield seq


def maybe_int(arg):
    """Return the corresponding int if the arguments represents one, or None."""
    try:
        return int(arg)
    except:
        return None


def is_int(arg):
    """Return True if the arguments represents an int, or False.
    
    The argument may be not an int (maybe e.g. a string), but if it
    can be cast to an int, it represents an int.

    """
    return maybe_int(arg) is not None


