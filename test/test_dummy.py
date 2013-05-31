__author__ = 'Horace'

import unittest
import code
from code import index

class TestNumbers(unittest.TestCase):
    def test_one(self):
        codeTest = index()
        self.assertEqual(codeTest.func(3), 4)

def test_two():
    assert index.func(5) == 6