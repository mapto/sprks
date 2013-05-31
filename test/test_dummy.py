__author__ = 'Horace'

import unittest



class TestNumbers(unittest.TestCase):
    def test_one(self):
        import dummy_class
        codeTest = dummy_class.index()
        self.assertEqual(codeTest.func(3), 4)