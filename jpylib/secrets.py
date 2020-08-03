#!/usr/bin/env python3

import os
import sys
import zlib
import fcntl
import base64
import shutil
import collections
from datetime import datetime

from .alerts import notice, debug_vars

# Where to look for the secrets file.
basedir = "/" if os.geteuid() == 0 else os.environ.get('HOME')
default_filename = os.path.join(basedir, "etc/secrets")

# suffix of backup file
backup_suffix = ".backup"

# prefix of end line
end_prefix = "# written by putsecret() "

# Default character encoding to use; this *should* depend on the environment,
# but I am too lazy to do that now.
default_char_encoding = "utf-8"

# En- and decoder functions. The names must be {en,de}code_{tag}.

def encode_b64(data):
    """Encode data in base64."""
    return base64.b64encode(data)

def decode_b64(data):
    """Decode base64-encoded data."""
    return base64.b64decode(data)

def decode_zip(data):
    """Decode a zipped string. Implies base64 encoding of zip data."""
    zipped = decode_b64(data)
    return zlib.decompress(zipped)

def encode_zip(data):
    """Zip-compress data. Implies base64 encoding of zip data."""
    zipped = zlib.compress(data)
    return encode_b64(zipped)


# encode/decode direction
dir_encode = 0
dir_decode = 1
de_en_prefix = ["encode_", "decode_"]
    
def find_coder_func(option, direction):
    coder_name = de_en_prefix[direction] + option
    coder_func = globals().get(coder_name)
    if coder_func:
        return coder_func
    notice("secrets: encountered unknown option '{}'".format(option))
    return None


def maybe_decode(fields, key, char_encoding):
    """Decode the found value, if options are present.

    `fields`         the fields after the key, value only or with options;
    `key`            the key we originally searched for;
    `char_encoding`  the bytes => string encoding to use.
    """
    assert 1 <= len(fields) <= 2
    if len(fields) == 2:
        options, string = fields
        string = string.rstrip()
        if options:                       # skip an empty string => no options
            for opt in options.split(","):
                coder_func = find_coder_func(opt, dir_decode)
                if coder_func:
                    data = coder_func(bytes(string, char_encoding))
                    string = str(data, char_encoding)
                else:
                    string = ":".join([options, string])
    else:
        return fields[0].rstrip()
    return string


def putsecret(key, value, fname=None, options=[],
              char_encoding=default_char_encoding):
    """Put a secret tagged with `key` into the secrets file `fname`."""
    fname = fname or default_filename
    entries = collections.OrderedDict()
    shutil.copy2(fname, fname + backup_suffix)
    with open(fname) as f:
        newfile = os.path.join(os.path.dirname(fname),
                               "." + os.path.basename(fname) + ".newtmp")
        with open(newfile, "x") as out:
            try:
                os.chmod(newfile, 0o600)
                for line in f:
                    if line.startswith(end_prefix):
                        continue
                    tag, *rest = line.rstrip().split(":", 2)
                    if tag in entries:
                        notice("putsecret: ignoring additional entry for '{}'"
                               .format(tag))
                    else:
                        entries[tag] = rest
                for opt in options:
                    data = bytes(value, char_encoding)
                    data = find_coder_func(opt, dir_encode)(data)
                    value = str(data, char_encoding)
                entries[key] = [",".join(options), value]
                for key, fields in entries.items():
                    print(":".join([key, *fields]), file=out)
                print(end_prefix + datetime.now().isoformat(timespec="seconds"),
                      file=out)
                os.rename(newfile, fname)
            finally:
                try:
                    os.remove(newfile)
                except:
                    pass


def getsecret(key, fname=None, char_encoding=default_char_encoding):
    """Get a secret tagged with `key` from the secrets file `fname`.

    The default pathname for the secrets file is `/etc/secrets` if
    called by root, and `$HOME/etc/secrets` for normal users.

    The file consist of lines of the form `_key_:_value_`, so the key
    may not contain a colon. Whitespace is significant except at the end
    of the line, where it will be stripped, so the secret may not end
    with whitespace. You can get around these limitations by encoding
    key and/or value with e.g. base64.

    If the key is found, the value is returned. Otherwise, a `KeyError`
    exception is raised. The exception's arguments are a format string,
    the key, and the file name. (Splitting this up allows for subsequent
    i18n.)

    If the found value for the key starts with "{b64}", it will be
    base64-decoded before it is returned.

    """
    if fname is None:
        fname = default_filename
    try:
        os.chmod(fname, 0o600)
    except:
        pass
    with open(fname) as f:
        for line in f:
            tag, *rest = line.split(":", 2)
            if rest and tag == key:
                return maybe_decode(rest, key, char_encoding)
    raise KeyError("cannot find secret for '{}' in '{}'", key, fname)


def main():
    if not (2 <= len(sys.argv) <= 3):
        sys.exit("usage: getsecret key [filename]")
    try:
        print(getsecret(*sys.argv[1:]))
    except Exception as e:
        sys.exit("getsecret: " + e.args[0].format(*e.args[1:]))


if __name__ == '__main__':
    main()
