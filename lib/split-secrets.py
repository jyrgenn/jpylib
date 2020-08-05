#!/usr/bin/env python3

import json

secrets_file = "lib/secrets"
max_fields = 2
valid_opts = ("b64", "zip")

with open(secrets_file) as s:
    secrets = {}
    for line in s:
        key, *rest = line.rstrip().split(":", max_fields)
        if len(rest) == 0:
            continue
        if len(rest) == 1:
            secrets[key] = dict(value=rest[0], opts=None)
        else:
            assert len(rest) == max_fields, \
                f"unexpected length of rest: {len(rest)}"
            field1, value = rest
            all_valid = True
            maybeopts = field1.split(",")
            for opt in maybeopts:
                if opt not in valid_opts:
                    all_valid = False
                    break
            if all_valid:
                secrets[key] = dict(opts=maybeopts, value=value)
            else:
                secrets[key] = dict(opts=None, value=field1+":"+value)
print(json.dumps(secrets))
                
            
