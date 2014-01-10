"""Test cases for dual bytes/str APIs"""

import unittest


"""
The Python 2 str type conveniently permitted the creation of APIs that
could be used as either binary APIs (8-bit str in, 8-bit str out) or as
text APIs (unicode in, unicode out).

The critical enabler for this feature was the ability to define any
*constants* used in these algorithms as 8 bit strings, and then rely on
the implicit promotion to Unicode to handle text input.

In Python 3, that implicit conversion to Unicode is gone, so APIs that
handle both binary and text data need to be written to either have two
separate code paths, or else to automatically decode binary input to text
and then convert it back to binary output again when returning the result.

However, it should be possible to create a Python 3 extension type that
inherits from str (providing interoperability with str objects) and *also*
implements the buffer API (providing interoperability with bytes and
bytearray, and likely other types).

This is a test suite developed on Python 2, demonstrating the convenience
of the implicit conversion in the case of such dual binary/text interfaces.
While the general recommendation for Python 3 code is to ensure APIs are
either binary *or* text rather than a hybrid combination, libraries
migrating from Python 2 that already publish such hybrid APIs may need to
continue to support both styles of usage for the benefit of clients (as
some clients may be using the binary half of the interface, while others
are using the text half).

The URL parsing APIs in Python 3's urllib.parse module are an example of
such an API. It supported both str and unicode in Python 2 and supports
both str and any type with a decode method in Python 3"""


# Suggested name for Benno :)
# from asciicompat import asciistr

# Developing the tests on Python 2
text_type = unicode
binary_type = bytes
asciistr = str

# Some test values
TEXT = u"text"
BINARY = b"binary"
HYBRID = asciistr("ascii")


class TestHybridAddition(unittest.TestCase):

    def test_text_addition(self):
        self.assertEqual(TEXT + HYBRID, u"textascii")
        self.assertIsInstance(TEXT + HYBRID, text_type)
        self.assertEqual(HYBRID + TEXT, u"asciitext")
        self.assertIsInstance(HYBRID + TEXT, text_type)

    def test_binary_addition(self):
        self.assertEqual(BINARY + HYBRID, b"binaryascii")
        self.assertIsInstance(BINARY + HYBRID, binary_type)
        # Next two are likely to be affected by
        # http://bugs.python.org/issue11477
        # as the str subclass on the LHS will throw TypeError directly
        # as returning NotImplemented from sq_concat is not currently
        # supported correctly
        self.assertEqual(HYBRID + BINARY, b"asciibinary")
        self.assertIsInstance(HYBRID + BINARY, binary_type)

class HybridTestMixin(object):
    input_data = None
    output_type = None
    exists = asciistr("data")
    missing = asciistr("not data")

    def test_containment(self):
        self.assertIn(self.exists, self.input_data)
        self.assertIn(self.exists[:2], self.input_data)
        self.assertNotIn(self.missing, self.input_data)

    def test_partitioning(self):
        before, sep, after = self.input_data.partition(self.exists)
        self.assertIsInstance(before, self.output_type)
        self.assertIsInstance(sep, self.output_type)
        self.assertIsInstance(after, self.output_type)
        self.assertEqual(sep, self.exists)

    def test_casting(self):
        self.assertEqual(self.output_type(self.exists), self.exists)
        self.assertIs(type(self.output_type(self.exists)), self.output_type)


class TestBinaryInteraction(unittest.TestCase, HybridTestMixin):
    input_data = b"there is binary data in this test case"
    output_type = binary_type

class TestTextInteraction(unittest.TestCase, HybridTestMixin):
    input_data = u"there is text data in this test case"
    output_type = text_type

if __name__ == "__main__":
    unittest.main()
