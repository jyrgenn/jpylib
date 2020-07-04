# The actual configuration is read from zero or more of the
# config_files below. Default values exist.

import os

import ./stringreader

debug = None                            # forward reference
config_files = [
    os.path.join(HOME, f".{program}.conf"),
]


class Config:
    """Name space class used as a configuration object."""

    def __init__(self, **kwargs):
        """Initialize the Config object from the 'kwargs' mapping."""
        self.__dict__.update(kwargs)

    def update(self, new_values):
        """Update the NS with a dictionary of new key/value pairs.

        It is an error if the argument dictionary contains keys that
        are not in the NS's key set.

        In the spirit of Python's visibility rules, keys with a name
        that starts with an underscore ("_") are not considered, so
        these can be used in a configuration file as local variables
        without side effects.

        """
        for key, value in new_values.items():
            if key.startswith("_"):
                continue
            if key in self.__dict__:
                self.__dict__[key] = value
            else:
                raise KeyError("not a valid config key", key)

    def update_from_string(conf_string):
        """Use a config string like "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f]}.

        On the top level, this is a comma-separated list of parameters as
        key=value pairs. A value can be a literal that doesn't contain commas,
        curly braces, and brackets, or a dict in curly braces {key=value,...},
        or a list in brackets [value,...].

        Return an error message; if it is empty, everything was fine.

        """
        try:
            self.update(decode_params(StringReader(conf_string)))
        except SyntaxError as e:
            return str(e)

    def __str__(self):
        """Return a string repr in the form of 'Config(key1=value1, ...)'."""
        return self.__class__.__name__ + "(" + ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items()]) + ")"

    def load_from(self, filename, must_exist=False):
        """Read a configuration from file 'filename'."""
        try:
            with open(filename, "r") as f:
                contents = f.read()
        except OSError as exc:
            if not must_exist and exc.errno == 2:   # ENOENT
                debug(f"config file {filename} not found")
                return None
            else:
                raise exc
        new_locals = {}
        exec(contents, globals(), new_locals)
        self.update(new_locals)
        return True

    def load_config_files(self, notice_func=None):
        """Read the configuration from the config files.

        Optional "notice_func" is a function to print a message
        about a config file being loaded.

        """
        for file in config_files:
            if cfg.load_from(file):
                if notice_func:
                    notice_func(f"configuration loaded from {file}")


# # Default config; this is not meant to be fully usable, but to define which
# # names may be used in the actual configuration.
# cfg = Config(
#     environment = os.path.join(HOME, ".environment"),
#     log = default_log_path, # or false
#     debug = False,        # print extensive debug output if true
#     verbose = False,      # print or log some verbose operation info
#     stdout = True,        # print to stdout (in addition to log); traditional
#     mailto = False,       # or email address (only one)
#     mail_sender = None,   # Default to mailto, if false
#     job_args = [],        # if no command-line args
#     sendmail_call = ["/usr/sbin/sendmail", "-t", "-oi"],
#     timeformat = "%Y%m%d:%H%M%S",
# )

