__author__ = 'Horace'

import unittest
from code import index

class MyTest(unittest.TestCase):
    def test(self):
        codeTest = index()
        self.assertEqual(codeTest.func(3), 4)

def test_answer():
    assert index.func(3) == 5