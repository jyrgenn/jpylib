#!/busr/bin/env python3

class Namespace:
    """Simple name space class."""

    def __init__(self, **kwargs):
        """Initialize a Namespace object from the 'kwargs' mapping."""
        self.__dict__.update(kwargs)

    def update(self, new_values, skip_underscore=False):
        """Update the NS with a dictionary of new key/value pairs.

        It is an error if the argument dictionary contains keys that
        are not in the NS's key set.

        If `skip_underscore` is true, keys with a name that starts with an
        underscore ("_") are not considered for update

        """
        for key, value in new_values.items():
            if key.startswith("_") and skip_underscore:
                continue
            if key in self.__dict__:
                self.__dict__[key] = value
            else:
                raise KeyError("not a valid config key", key)

    def __str__(self):
        """Return a string repr in the form of 'Namespace(key1=value1, ...)'."""
        return self.__class__.__name__ + "(" + ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items()]) + ")"

    def __repr__(self):
        return self.__str__()
