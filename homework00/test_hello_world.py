"""Works with text"""
import unittest

import hello_world


class HelloTestCase(unittest.TestCase):
    """Class to work with a definition"""
    def test_hello(self):
        """Works with messages"""
        m = "message"
        self.assertEqual(m, hello_world.text())
