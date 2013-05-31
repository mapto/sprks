__author__ = 'Horace'

import unittest
import code


class TestNumbers(unittest.TestCase):
    def test_one(self):
        codeTest = code.index()
        self.assertEqual(codeTest.func(3), 4)