import os
import unittest
from dictionary import infer

class TestDictionary(unittest.TestCase):

    def test_infer(self):
        schema = infer(os.getcwd() + "/data/sample.csv")
        
        self.assertEqual(schema.fields[0].name, "int" )
        self.assertEqual(schema.fields[1].name, "float" )
        self.assertEqual(schema.fields[2].name, "text" )
        self.assertEqual(schema.fields[3].name, "date_time" )

        self.assertEqual(schema.fields[0].type, "integer" )
        self.assertEqual(schema.fields[1].type, "number" )
        self.assertEqual(schema.fields[2].type, "string" )
        self.assertEqual(schema.fields[3].type, "string" )

if __name__ == '__main__':
    unittest.main()