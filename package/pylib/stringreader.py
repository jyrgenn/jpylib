# The StrBuf is used by the parser that interprets a parameters command.

class StringReader():
    """A class that lets the user read characters from the underlying string.

    Alas, io.StringIO doesn't have a straightforward eof() method, which would
    have made this implementation unnecessary.

    """
    def __init__(self, content):
        """Create a strBuf from a string."""
        self.content = content
        self.len = len(content)
        self.next = 0

    def pop(self):
        """Return the next character from the strBuf, or None at EOF."""
        if self.next < self.len:
            ch = self.content[self.next]
            self.next += 1
            return ch
        else:
            return None

    def eof(self):
        """Return True if the strBuf is at EOF."""
        return self.next >= self.len

    def __str__(self):
        """Return a string representation of a strBuf.

        The next character is marked by a preceding '^'; this will of course be
        not very helpful with a string containing this character.

        """
        head = self.content[:self.next]
        tail = self.content[self.next:]
        show = head + "^" + tail
        return f"<{self.__class__.__name__} {repr(show)}>"

