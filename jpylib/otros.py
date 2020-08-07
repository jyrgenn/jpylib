# assorted smallish functions

means_true = "yes y ja j klar si claro on true aye 1 affirmative".split()
means_false = "no n nein off false nay 0 negative".split()

def boolish(value, default=None):
    """Return a truth value for the argument.

    If that cannot be determined, fall back to default (if not None) or raise a
    ValueError exception. This can be used for parsing config files (that aren't
    Python) or interactive answers or the like.

    """

    value = value.lower()
    if value in means_true:
        return True
    if value in means_false:
        return False
    if default is None:
        raise ValueError("value '{}' cannot be understood as false or true".
                         format(value))
    else:
        return default
