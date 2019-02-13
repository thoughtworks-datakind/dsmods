import os
import json
import unittest
import dictionary
from collections import OrderedDict


class TestDictionary(unittest.TestCase):

    def test_infer(self):
        actual_json = json.dumps(dictionary.infer(os.getcwd() + "/data/sample.csv"), default=lambda x: x.__dict__,
                                 sort_keys=True)

        with open('./schema.json') as f:
            expected_json = json.dumps(json.load(f, object_pairs_hook=OrderedDict))

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
