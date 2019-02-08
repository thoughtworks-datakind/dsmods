import os
import unittest
from dictionary import infer
import pandas as pd

class TestDictionary(unittest.TestCase):

    def test_infer(self):
        actual = infer(os.getcwd() + "/data/sample.csv")
        expected = pd.read_csv(os.getcwd() + "/data/schema.csv")
        expected.set_index("attribute", inplace=True)
        self.assertTrue(expected.equals(actual))

if __name__ == '__main__':
    unittest.main()