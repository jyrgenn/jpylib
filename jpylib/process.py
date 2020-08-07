# -*- python -*-

# Do things with processes.

import subprocess


def backquote(command, touchy=False, shell=None, stdout_only=True):
    """Similar to Perl's `command` feature: run process, return result.

    If we are touchy, we raise an exception at the slightest provocation, i.e.
    non-empty stderr output or non-zero exit status.

    If command is a tuple or a list, run it directly. Otherwise, make it a
    string if necessary and:
    
        If shell is True, run command as shell command line with "/bin/sh".

        If shell is otherwise true, use it as the shell and run command in it.
    
        If shell is None (or unspecified), run command with "/bin/sh" if it
        contains shell meta characters. Otherwise, split the string into a list
        and run it directly.

        If run_shell is otherwise false, split the string into a list and run it
        directly.

    If stdout_only is true (the default), return stdout only. Otherwise, a tuple
    of (stdout, stderr, exit status).

    """
    shellmeta = "\"'`|&;[(<>)]*? \t"
    if not isinstance(command, (list, tuple)):
        command = str(command)
        if shell:
            if shell is True:
                shell = "/bin/sh"
            command = [shell, "-c", command]
        elif shell is None:
            if any([ ch in shellmeta for ch in command ]):
                command = [shell, "-c", command]
            else:
                command = command.split()
        else:
            command = command.split()

    with subprocess.Popen(command, stdin=subprocess.DEVNULL,
                          stderr=subprocess.PIPE,
                          stdout=subprocess.PIPE) as proc:
        proc.wait()
        result = (proc.stdout.read().decode("utf-8"),
                  proc.stderr.read().decode("utf-8"),
                  proc.returncode)
        if touchy and (result[1] or result[2]):
            raise ChildProcessError("command {} exited status {}; stderr: '{}'"
                                    .format(command, result[2], result[1]))
    if stdout_only:
        return result[0]
    return result
