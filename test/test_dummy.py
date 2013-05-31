__author__ = 'Horace'

import unittest
import dummy_class


class TestNumbers(unittest.TestCase):
    def test_one(self):
        codeTest = dummy_class.index()
        self.assertEqual(codeTest.func(3), 4)