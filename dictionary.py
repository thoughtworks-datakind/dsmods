import json
import numpy as np
import pandas as pd
from tableschema import Table
from dateutil.parser import parse

def infer(path, limit = 2000):
    table = Table(path)
    table.infer(limit=limit, confidence=0.75)
    return convert_to_df(table.schema)

def convert_to_df(schema):
    names = ["name"]
    types = ["type"]
    formats = ["format"]

    for field in schema.fields: 
        names.append(field.name)
        types.append(field.type)
        formats.append(field.format)

    data = np.array([names, types, formats])
    df = pd.DataFrame(data=data[1:,1:], index=data[1:,0], columns=data[0,1:])
    df.index.name = "attribute"
    return df