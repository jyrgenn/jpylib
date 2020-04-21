#!/usr/bin/env python3

import pgetopt

indent_level = "  "

prob = None                     # predecl
tests = []

def prit(it, indent=""):
    brk = "[]" if isinstance(it, list) else "()"
    print(f"{indent}{brk[0]}")
    n_indent = indent + indent_level
    for el in it:
        prob(el, indent=n_indent)
    print(f"{indent}{brk[1]}")    

def prkv(dic, indent=""):
    print(f"{indent}{{")
    n_indent = indent + indent_level
    for k, v in dic.items():
        print(f"{n_indent}{repr(k)}: ", end="")
        prob(v, n_indent)
    print(f"{indent}}}")

def prob(ob, indent=""):
    if isinstance(ob, (list, tuple)):
        prit(ob, indent)
    elif isinstance(ob, dict):
        prkv(ob, indent)
    else:
        print(f"{indent}{repr(ob)}")
        

def pr(*args):
    print(*args, end=" ", flush=True)

def eq(a1, a2):
    return a1 is a2

def equal(a1, a2):
    return a1 == a2

def typ(a1, a2):
    return type(a1) is type(a2)

def check(what, real, expected, op):
    #print(f"check {what}: {real} ~ {expected}")
    if op(real, expected):
        pr("|", what, "ok")
        return 0
    else:
        pr(what, "DIFFERS:", real)
        return 1


def run_test(testdef):
    testname, desc, *cases = testdef
    for case in cases:
        c_name, c_argv, c_values, c_errtype, c_args = case
        pr(f"{testname}: {c_name:12}")
        errors = 0
        r_errtype = r_ovc = r_args = r_e = None
        try:
            r_ovc, r_args = pgetopt.parse(desc, c_argv, exit_on_error=False)
        except (IndexError, KeyError, TypeError) as e:
            r_e = e
        except Exception as e:
            raise(e)
        if r_e:
            errors += check("etype", type(r_e), c_errtype, eq)
            print("FAIL" if errors else "OK")
            continue
        #pr("c_values:", c_values, "c_errtype", c_errtype, "r_ovc:", r_ovc)
        if c_values is None:
            errors += check("ovc", r_ovc, None, eq)
            continue
        #prob(tests[0][1])
        errors += check("values", r_ovc.values(), c_values, equal)
        errors += check("args", r_args, c_args, equal)
        print("FAIL" if errors else "OK")
    return errors


# name, desc{}, *args_values[ (name, args[], values[], exception type, args), ]
tests = [
    ("d0",
     {
         "s": ("schmooze", bool, 0, "increase schmooziness"),
         "o": ("output_file", str, None, "output file (or stdout)", "NAME"),
         "n": ("repetitions", int, 3, "number of repetitions"),
         "d": ("debug", str, [], "debug topics", "DEBUG_TOPIC"),
         "_arguments": ("string_to_print", "..."),
         "_help_header": "print a string a number of times",
         "_help_footer": "This is just an example program.",
     },
     # per test case:
     # case name, passed argv, expected values, exp. exception, exp. args
     ("no args", [], None, IndexError, None),
     ("1 arg", ["huhu"],
      dict(schmooze=0, output_file=None, repetitions=3, debug=[]),
      None, ["huhu"]),
     ("5 args", ["huhu", "haha", "dada", "dodo", "bu"],
      dict(schmooze=0, output_file=None, repetitions=3, debug=[]),
      None, ["huhu", "haha", "dada", "dodo", "bu"]),
     ("1 arg -ss", ["-ss", "huhu"],
      dict(schmooze=2, output_file=None, repetitions=3, debug=[]),
      None, ["huhu"]),
     ("wrong opt", ["-d", "print", "--output_file=hamburg", "haha", "dada"],
      None, KeyError, ["haha", "dada"]),
     ("more opts", ["-d", "print", "--output-file=hamburg", "haha", "dada"],
      dict(schmooze=0, output_file="hamburg", repetitions=3, debug=["print"]),
      None, ["haha", "dada"]),
     ("no opts", ["--", "-d", "print", "--output_file=hamburg", "haha", "dada"],
      dict(schmooze=0, output_file=None, repetitions=3, debug=[]),
      None, ["-d", "print", "--output_file=hamburg", "haha", "dada"])
    ),
]

if __name__ == "__main__":
    total_errors = 0
    for test in tests:
        total_errors = run_test(test)

    s = "" if total_errors == 1 else "s"
    print()
    if total_errors:
        print(f"FAIL, {total_errors} total error{s}")
    else:
        print("OK all good")
