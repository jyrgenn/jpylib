import sys
import unittest
from jpylib.capture import outputCaptured, outputAndExitCaptured

class CaptureTest(unittest.TestCase):

    def test_capture(self):
        """Test outputCaptured()."""
        with outputCaptured() as (out, err):
            print("huhu")
            print("hihi", file=sys.stderr)
        self.assertEqual(out.getvalue(), "huhu\n")
        self.assertEqual(err.getvalue(), "hihi\n")

    def test_capture_exit(self):
        with outputAndExitCaptured() as (out, err, status):
            print("hohoho")
            print("hihihi", file=sys.stderr)
            sys.exit("hahaha")
        self.assertEqual(out.getvalue(), "hohoho\n")
        self.assertEqual(err.getvalue(), "hihihi\n")
        self.assertEqual(status.value, "hahaha")

    def test_capture_none(self):
        """Test capture no sys.exit."""
        with outputAndExitCaptured() as (out, err, status):
            print("hohoho")
            print("hihihi", file=sys.stderr)
        self.assertEqual(out.getvalue(), "hohoho\n")
        self.assertEqual(err.getvalue(), "hihihi\n")
        self.assertEqual(status.value, None)

