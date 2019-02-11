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

        metadata.missing_count = data[field.name].isnull().sum()
        metadata.missing_percentage =  round(float(metadata.missing_count)/num_rows  * 100 , 2)
        metadata.distinct_count = data[field.name].nunique()
        metadata.distinct_percentage = round(float(data[field.name].nunique()) / (num_rows - data[field.name].isnull().sum()) * 100, 2)
        metadata.most_frequent = data[field.name].value_counts().idxmax()

        if metadata.type == "string" and metadata.missing_percentage != 100.0:
            if rows_to_scan == data[field.name].head(rows_to_scan).apply(lambda x :is_date(x)).sum():
                metadata.type = "date"

        metadata_array.append(metadata)

    return metadata_array

class Metadata:

    name = ""
    type = ""
    format = ""
    missing_count = 0
    missing_percentage = 0.0
    distinct_count = 0
    distinct_percentage = 0.0
    most_frequent = object()