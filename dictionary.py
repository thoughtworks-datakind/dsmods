import pandas as pd
from tableschema import Table
from dateutil.parser import parse

def is_date(string):
    if str(string) == "":
        return True
    try: 
        parse(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def infer(path, limit = 2000):
    table = Table(path)
    table.infer(limit=limit, confidence=0.75)

    data = pd.read_csv(path, low_memory=False)
    rows_to_scan = limit if limit < data.index._stop else data.index._stop

    metadata_array = []
    for field in table.schema.fields: 
        metadata = Metadata()
        metadata.name = field.name
        metadata.type = field.type 
        metadata.format = field.format

        if field.type == "string" and rows_to_scan == data[field.name].head(rows_to_scan).apply(lambda x :is_date(x)).sum() :
            metadata.type = "date"
        metadata_array.append(metadata)

    return metadata_array

class Metadata:

    name = ""
    type = ""
    format = ""