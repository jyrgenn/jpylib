
import collections

def avg_median(values):
    """Return the median value of the passed numeric values."""
    n = len(values)
    half = int(n / 2)
    if n % 2:
        return values[half]
    return (values[half] + values[half-1]) / 2


def avg_mean(values):
    """Return the mean value of the passed numeric values."""
    return sum(values) / len(values)


def avg_mode(values):
    """Return the mode (most frequent) value of the passed numeric values.

    If there are multiple values occuring most frequently, return any of them.
    For an empty sequence of values, return None.
    """
    counts = collections.Counter(values)
    mode = None
    cmax = 0
    for value, count in counts.items():
        if count > cmax:
            mode = value
            cmax = count
    return mode


def avg_midrange(values):
    """Return the arithmetic mean of the highest and lowest value of values."""
    vmin = min(values)
    vmax = max(values)
    return (vmin + vmax) / 2


def sans_outliers(values):
    """Return a copy of the values with the highest and lowest value removed.

    If there is more than one highest or lowest value, only one of them is
    removed.

    """
    vmax = None
    vmin = None
    for value in values:
        if vmin is None or value < vmin:
            vmin = value
        if vmax is None or value > vmax:
            vmax = value
    new_values = values.copy()
    if new_values:
        new_values.remove(vmin)
    if new_values:
        new_values.remove(vmax)
    return new_values


def maybe_int(arg):
    """Return the corresponding int if the arguments represents one, or None."""
    try:
        return int(arg)
    except:
        return None


def maybe_num(arg):
    """Return the corresponding int or float if arg represents one, or None."""
    the_int = maybe_int(arg)
    if the_int is None:
        try:
            return float(arg)
        except:
            return None
    return the_int


def is_int(arg):
    """Return True if the arguments represents an int, or False.
    
    The argument may be not an int (maybe e.g. a string), but if it
    can be read as an int, it represents an int.

    """
    return maybe_int(arg) is not None


def is_num(arg):
    """Return True if the arguments represents a number, or False.
    
    The argument may be not numeric (maybe e.g. a string), but if it
    can be read as a number, it represents a number.

    """
    return maybe_num(arg) is not None


