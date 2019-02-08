import os
import unittest
import json
import dictionary
import pandas as pd

class TestDictionary(unittest.TestCase):

    def test_infer(self):
        actual = dictionary.infer(os.getcwd() + "/data/sample.csv")
        actual_json = json.dumps(actual, default=lambda x: x.__dict__)

        expected_json = ('['
        '{"type": "integer", "name": "column_int", "format": "default"}, '
        '{"type": "number", "name": "column_float", "format": "default"}, '
        '{"type": "string", "name": "column_text", "format": "default"}, '
        '{"type": "date", "name": "column_date_time", "format": "default"}'
        ']')
        
        self.assertEquals(expected_json, actual_json)

    def test_is_date(self):
        self.assertTrue(dictionary.is_date("23/02/2019"))
        self.assertTrue(dictionary.is_date("23/02/19"))
        self.assertTrue(dictionary.is_date(""))

        self.assertFalse(dictionary.is_date("abcdefgh"))
        self.assertFalse(dictionary.is_date(20.0))
        self.assertFalse(dictionary.is_date(20))

if __name__ == '__main__':
    unittest.main()