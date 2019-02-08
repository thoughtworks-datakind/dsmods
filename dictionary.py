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
    num_rows = data.index._stop
    
    rows_to_scan = limit if limit < num_rows else num_rows

    metadata_array = []
    for field in table.schema.fields: 
        metadata = Metadata()
        metadata.name = field.name
        metadata.type = field.type 
        metadata.format = field.format

        if field.type == "string" and rows_to_scan == data[field.name].head(rows_to_scan).apply(lambda x :is_date(x)).sum() :
            metadata.type = "date"
        
        metadata.missing_count = data[field.name].isnull().sum()
        metadata.missing_percentage =  round(float(metadata.missing_count)/num_rows  * 100 , 2)

        metadata_array.append(metadata)

    return metadata_array

class Metadata:

    name = ""
    type = ""
    format = ""
    missing_count = 0
    missing_percentage = 0.0