#!/usr/bin/env python3

# Read the secrets file and print the data as a JSON structure. These values are
# used by the test procedures to compare against the results of getsecret().
# This is, of course, not foolprof, but at least a second and I think different
# enough implementation.

import json

secrets_file = "tmp/secrets"
max_fields = 2
valid_opts = ("b64", "zip")

with open(secrets_file) as s:
    secrets = {}
    for line in s:
        key, *rest = line.rstrip().split(":", max_fields)
        if len(rest) == 0:
            # not a valid key:[opts:]value line at all
            continue
        if len(rest) == 1:
            # no options, obviously, so the secret is the value
            value = rest[0]
            secrets[key] = dict(value=value, opts=None, secret=value)
        else:
            # While in this case we have three fields separated by colons, the
            # second need not be options.
            assert len(rest) == max_fields, \
                f"unexpected length of rest: {len(rest)}"
            field1, value = rest
            all_valid = True
            maybeopts = list(filter(None, field1.split(",")))
            for opt in maybeopts:
                # beware, opt may be empty
                if opt and opt not in valid_opts:
                    all_valid = False
                    break
            if all_valid:
                # this includes the case of an empty field1
                secrets[key] = dict(opts=maybeopts or None,
                                    value=value, secret=None)
            else:
                # field1 is not all valid options, so it is actually part of the
                # value
                value = field1+":"+value
                secrets[key] = dict(opts=None, value=value, secret=value)
print(json.dumps(secrets, indent=4))
                
            
